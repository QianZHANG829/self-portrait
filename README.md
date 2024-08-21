

# Syphon Camera Feed with Delay

This project captures live video from a camera and introduces a delay effect using frame buffers. It allows for the real-time blending of buffered video frames with the live feed and supports multiple buffer loops for different delay intervals.

## Features

- Captures live video feed from a camera (e.g., iPhone camera).
- Creates a delay effect by buffering video frames.
- Supports multiple buffers to create different delay loops.
- Blends buffered frames with the live video feed.
- Publishes the video stream using the Syphon Metal Server.

## Installation

### Prerequisites

- Python 3.6 or later
- macOS (required for Syphon functionality)

### Steps

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/syphon-camera-delay.git
    ```
2. Navigate to the project directory:
    ```bash
    cd syphon-camera-delay
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
4. **macOS users**: Install the Syphon Python library:
    ```bash
    pip install syphon-python
    ```
    - [Syphon Python Library Documentation](https://pypi.org/project/syphon-python/)

## Usage

1. Connect your camera (e.g., iPhone) to your computer.
2. Run the script:
    ```bash
    python syphon_camera_feed.py
    ```
3. The live camera feed will start with the configured delay and buffering effects.

4. Press `q` to quit the application.

## Parameters

- `buffer_count`: Set the number of buffers to create for different delay loops. Modify the `x` variable in the script to change the buffer count.
- `max_buffer_frames`: The number of frames to buffer, which determines the delay time. Adjust this to control the length of each delay.

## Example

```python
x = 10  # Set the number of buffers (loops)
main(buffer_count=x)
```

## Troubleshooting

- Ensure that the camera is connected and recognized by your system.
- If the video feed is slow or delayed, consider reducing the buffer size or the number of buffers.
- If you encounter issues with Syphon on macOS, make sure the `syphon-python` library is correctly installed.

## Contributing

Feel free to submit issues or pull requests to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This updated README now includes instructions for installing the `syphon-python` library and provides a reference link for macOS users. You can update your GitHub repository with this new README file.
