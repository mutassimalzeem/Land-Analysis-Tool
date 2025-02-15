# Land Analysis Tool 🌍

A Python-based desktop application for analyzing land characteristics, pollution levels, and soil types across different regions. This tool helps environmental agencies, real estate developers, and land management professionals make informed decisions about land use.

## 🌟 Features

### Data Management
- SQLite database for persistent data storage
- Add individual land records with region, pollution level, and soil type
- Import data from CSV and Excel files
- Export functionality to save data as CSV

### Analysis Capabilities
- Custom pollution level thresholds
- Soil type filtering
- Real-time analysis updates
- Detailed results view

### Visualization
- Interactive bar charts
- Color-coded soil type representation
- Dynamic legend updates
- Customizable pollution level analysis

## 🛠️ Technical Requirements

- Python 3.8+
- Required packages:
  ```
  numpy
  pandas
  matplotlib
  tkinter
  sqlite3
  ```

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mutassimalzeem/land-analysis-tool.git
   cd land-analysis-tool
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## 🎯 Usage

### Data Input
1. Launch the application
2. Navigate to the "Data Input" tab
3. Enter data manually or import from CSV/Excel
4. View current data in the table below

### Visualization
1. Go to the "Visualization" tab
2. View the color-coded bar chart
3. Use the "Refresh Plot" button to update after data changes

### Analysis
1. Select the "Analysis" tab
2. Set maximum pollution level
3. Choose suitable soil types
4. Click "Run Analysis" to see filtered results

## 📊 Data Format

### CSV/Excel Import Format
Your import files should have the following columns:
- Region (text)
- Pollution Level (numeric)
- Soil Type (text: Fertile/Rocky/Neutral/Sandy)

Example:
```csv
Region,Pollution Level,Soil Type
North,15.5,Fertile
South,25.0,Rocky
```

## 🎨 Color Coding

Soil types are represented by different colors:
- Fertile: Green
- Rocky: Brown
- Neutral: Blue
- Sandy: Yellow

## 💡 Use Cases

- Environmental monitoring
- Land development planning
- Agricultural suitability analysis
- Urban development projects
- Conservation planning

## 🔍 Project Structure

```
land-analysis-tool/
│
├── main.py                   # Main application file
├── requirements.txt          # Dependencies
├── README.md                # Documentation
│
└── Day 84/                  # Project directory
    └── land_data.db         # SQLite database
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Inspired by environmental conservation needs
- Built with Python and its amazing ecosystem of libraries

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/mutassimalzeem)

Project Link: [https://github.com/mutassimalzeem/land-analysis-tool](https://github.com/mutassimalzeem/land-analysis-tool)
