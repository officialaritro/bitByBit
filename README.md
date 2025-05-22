# bitByBit - YouTube Downloader

A user-friendly desktop application for downloading YouTube videos using `yt-dlp`. This application provides a graphical interface to easily download videos in various formats and qualities. No ADS, No queues, Hassle-free, easy-to-use, No getting redirected to sketchy websites that steal
your personal data.

## Features

- **Easy-to-use GUI**: Clean and intuitive interface built with Tkinter
- **Multiple Format Support**: Download videos in various resolutions and formats
- **Format Selection**: View all available formats with detailed information (resolution, file size, codec)
- **Real-time Progress**: Live download progress with speed and ETA information
- **Download Logging**: Detailed logs for troubleshooting
- **Custom Save Location**: Choose where to save your downloaded videos
- **Reliable Downloads**: Uses `yt-dlp` for stable and up-to-date YouTube downloading

## Demo

![YouTube Downloader Interface](bitByBit.mp4)
*Main interface showing video information and format selection*

## Requirements

- Python 3.7 or higher
- `yt-dlp` library
- `tkinter` (usually comes with Python)

## Installation

1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/yourusername/bitByBit.git
   cd bitByBit
   ```

2. **Install required dependencies**:
   ```bash
   pip install yt-dlp
   ```

3. **Run the application**:
   ```bash
   python youtube_downloader.py
   ```

## Usage

### Quick Start

1. **Launch the application**: Run the Python script
2. **Enter YouTube URL**: Paste any YouTube video URL in the input field
3. **Fetch Video Info**: Click "Fetch Video Info" to load available formats
4. **Select Format**: Choose your preferred format from the table
5. **Choose Location**: Select where to save the video (defaults to Downloads folder)
6. **Download**: Click "Download" to start downloading

### Understanding Format Selection

The format table shows:
- **Format ID**: Internal identifier for the format
- **Format**: File extension (mp4, webm, etc.)
- **Resolution**: Video quality (1080p, 720p, etc.)
- **File Size**: Approximate download size
- **Notes**: Additional information (audio only, video only, etc.)

### Format Types Explained

- **Normal**: Combined video and audio in one file
- **Video Only**: Video stream without audio (requires separate audio download)
- **Audio Only**: Audio stream only
- **DASH**: Dynamic Adaptive Streaming format

## Supported URLs

This application supports various YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- YouTube playlist URLs (downloads individual videos)

## Features in Detail

### Progress Tracking
- Real-time download progress bar
- Download speed display
- Estimated time remaining (ETA)
- Current status updates

### Logging System
- Detailed download logs
- Error messages and warnings
- Progress information
- Troubleshooting information

### Error Handling
- Graceful handling of network issues
- Clear error messages
- Automatic UI state management
- Recovery from failed downloads

## Troubleshooting

### Common Issues

1. **"No formats available" error**:
   - The video might be private or restricted
   - Try updating yt-dlp: `pip install --upgrade yt-dlp`

2. **Download fails with network error**:
   - Check your internet connection
   - Some videos might be geo-restricted
   - Try a different video to test

3. **Application won't start**:
   - Ensure Python 3.7+ is installed
   - Make sure yt-dlp is installed: `pip install yt-dlp`
   - Check if tkinter is available (should come with Python)

4. **Slow downloads**:
   - This depends on your internet speed and YouTube's servers
   - Try downloading during off-peak hours

### Getting Help

If you encounter issues:
1. Check the download log in the application
2. Update yt-dlp to the latest version
3. Try with a different video URL
4. Check the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp)

## Technical Details

### Dependencies
- **yt-dlp**: Modern YouTube downloading library (fork of youtube-dl)
- **tkinter**: GUI framework (included with Python)
- **threading**: For non-blocking downloads
- **os**: File system operations

### Architecture
- **Main Thread**: Handles UI and user interactions
- **Worker Threads**: Handle video info fetching and downloading
- **Progress Callbacks**: Update UI from download threads
- **Error Handling**: Comprehensive error catching and user feedback

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/yourusername/bitByBit.git
cd bitByBit
pip install yt-dlp
python bitByBit.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download or that are in the public domain.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful YouTube downloading library
- [Python Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework
- YouTube - Video platform

## Changelog

### v1.0.0 (Current)
- Initial release with yt-dlp integration
- GUI interface with format selection
- Progress tracking and logging
- Error handling and recovery
- Custom save location support

## Future Enhancements

- [ ] Playlist downloading support
- [ ] Audio-only download presets
- [ ] Download queue management
- [ ] Settings/preferences panel
- [ ] Theme customization
- [ ] Download history
- [ ] Automatic quality selection
- [ ] Subtitle downloading
- [ ] Update checker

## Support

For support, please:
1. Check the troubleshooting section above
2. Look through existing issues on GitHub
3. Create a new issue with detailed information about your problem

---

**Note**: This application is not affiliated with YouTube or Google. It's an independent tool that uses publicly available libraries to download content.