# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Tuple, Dict, List
from pydantic import BaseModel, Field

try:
    import manga_translator
except ImportError:
    '''Ignored'''

from manga_translator.config import Config
from manga_translator.ocr import dispatch as dispatch_ocr, prepare as prepare_ocr
from manga_translator.utils import Quadrilateral

import logging
import uvicorn
import os
import cv2
import numpy as np
import asyncio


config = Config()
device = 'cpu'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def initialize():
    await prepare_ocr(config.ocr.ocr, device)


class BoundingBox(BaseModel):
    name: str = Field(..., description="탐지된 객체의 이름")
    top_left: Tuple[int, int]
    top_right: Tuple[int, int]
    bottom_right: Tuple[int, int]
    bottom_left: Tuple[int, int]

class VideoFrameOcrRequest(BaseModel):
    video_path: str = Field(..., description="분석할 비디오 파일의 전체 경로")
    frame_number: int = Field(..., gt=0, description="프레임 번호")
    boxes: List[BoundingBox] = Field(..., description="탐지된 바운딩 박스 리스트")

class VideoFrameOcrResponse(BaseModel):
    map: Dict[str, str] = Field(..., description="탐지된 객체의 이름과 탐지된 텍스트의 매핑")


async def ocr_img(img_rgb: np.ndarray, boxes: List[BoundingBox]) -> Dict[str, str]:
    textlines = []
    for box in boxes:
        pts = np.array([box.top_left, box.top_right, box.bottom_right, box.bottom_left], dtype=np.int32)
        textlines.append(Quadrilateral(pts, '', 0))

    textlines = await dispatch_ocr(config.ocr.ocr, img_rgb, textlines, config.ocr, device, False)

    name_text_map: Dict[str, str] = {}
    for box, textline in zip(boxes, textlines):
        name_text_map[box.name] = textline.text

    return name_text_map


@app.post("/ocr/video-frame", response_model=VideoFrameOcrResponse)
async def ocr_api(request: VideoFrameOcrRequest) -> VideoFrameOcrResponse | None:
    video_path = request.video_path
    frame_number = request.frame_number
    boxes = request.boxes

    # --- 1. 비디오 파일 존재 확인 ---
    if not os.path.exists(video_path):
        logger.error(f"비디오 파일을 찾을 수 없음: {video_path}")
        raise HTTPException(status_code=404, detail=f"Video file not found: {video_path}")

    # --- 2. 비디오 프레임 추출 ---
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"비디오 파일을 열 수 없음: {video_path}")
        raise HTTPException(status_code=500, detail=f"Could not open video file: {video_path}")

    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()
        if not ret or frame is None:
            logger.error(f"프레임 읽기 실패: 비디오='{video_path}', 프레임 번호={frame_number}")
            raise HTTPException(status_code=500, detail=f"Failed to read frame at frame {frame_number}")

    except Exception as e:
        logger.error(f"프레임 추출 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error during frame extraction: {str(e)}")
    finally:
        cap.release()  # 비디오 캡처 객체 해제

    return VideoFrameOcrResponse(map=await ocr_img(frame, boxes))


if __name__ == "__main__":
    print(f"--- Starting FastAPI server (Single Process) ---")
    asyncio.run(initialize())
    port = int(os.environ.get("PYTHON_PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)