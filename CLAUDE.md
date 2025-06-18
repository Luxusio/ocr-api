# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OCR API service built on top of the manga-image-translator library. It provides a FastAPI-based web service that performs OCR (Optical Character Recognition) on specific regions of video frames. The primary use case is extracting text from bounding boxes within video frames for applications like gaming overlays or subtitle extraction.

## Architecture

The project consists of:
- **Main API Service** (`main.py`): FastAPI application with a single endpoint `/ocr/video-frame`
- **Dependency Mocking** (`mock_module.py`): Handles missing optional dependencies by creating dummy modules
- **Manga Image Translator Submodule**: Complete OCR/translation framework included as a git submodule
- **Build System** (`build.py`): PyInstaller configuration for creating standalone executables

Key architectural patterns:
- Uses the Model48pxOCR from manga-image-translator for OCR processing
- Implements a mock module system to handle optional dependencies gracefully
- Async/await pattern for OCR processing
- OpenCV for video frame extraction
- Pydantic models for request/response validation

## Common Commands

### Development Setup
```bash
# Initialize git submodules
git submodule update --init --recursive

# Install dependencies using uv
pip install uv
uv sync

# Install development dependencies
uv sync --group dev
```

### Running the Application
```bash
# Run the FastAPI server (default port 8967)
uv run main.py

# Run with custom port
PYTHON_PORT=8080 uv run main.py

# Run with debug mode (saves annotated frames)
DEBUG=1 uv run main.py
```

### Building
```bash
# Build standalone executable
uv run build.py
```

### Testing
The project includes Jupyter notebooks for testing:
- `notebooks/test_ocr.ipynb` - Basic OCR testing
- `notebooks/test_ocr_2.ipynb` - Additional OCR tests

Use the HTTP client configuration in `http/` directory to test the API endpoints.

## Key Files and Their Purpose

- `main.py`: Main FastAPI application with OCR endpoint
- `mock_module.py`: Dependency mocking system for optional packages
- `pyproject.toml`: Python project configuration with uv dependency management
- `manga_image_translator/`: Git submodule containing the core OCR functionality
- `build.py`: PyInstaller build configuration
- `http/OCR Video Frame.http`: HTTP client test file for API testing

## API Endpoint

**POST /ocr/video-frame**

Processes OCR on specified bounding boxes within a video frame.

Request model:
- `video_path`: Full path to video file
- `frame_number`: Frame number to extract (1-based)
- `boxes`: List of bounding boxes with names and coordinates

Response model:
- `map`: Dictionary mapping bounding box names to extracted text

## Environment Variables

- `DEBUG`: Set to '1' to enable debug mode (saves annotated frames)
- `PYTHON_PORT`: Custom port for the FastAPI server (default: 8967)

## Dependencies

The project uses a sophisticated dependency mocking system. The `mock_module.py` creates dummy modules for optional dependencies like PaddleOCR, pydensecrf, and various ML libraries that may not be available in all environments.

Primary dependencies are managed through uv and include:
- FastAPI for the web framework
- OpenCV for video processing
- PyTorch for ML models
- manga-image-translator as an editable local dependency