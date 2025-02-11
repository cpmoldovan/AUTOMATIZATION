# Contract Automation

This project automates contract generation using a simple web interface. Users can input contract details through an HTML form, and a Python server processes the data to generate a `.docx` file based on a predefined template.

## Features
- Web-based form for data input
- Automatic `.docx` document generation
- Local HTTP server for easy access
- Downloadable generated contracts

## Technologies Used
- Python
- Flask / HTTPServer (built-in Python module)
- docxtpl (for `.docx` template processing)
- HTML & CSS (Bulma framework for styling)

## Setup & Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/contract-automation.git
   cd contract-automation
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the server:
   ```sh
   python automatization.py
   ```

4. Open your browser and visit:
   ```sh
   http://127.0.0.1:8080
   ```

## File Structure
- `automatization.py` - Python script that runs the server and handles document generation
- `index.html` - Web interface for input
- `template.docx` - Word template for contract generation
- `documente_create/` - Folder where generated documents are stored

## Usage
1. Fill in the contract details in the web form.
2. Click "Generate Document" to create a `.docx` file.
3. Download the generated contract from the provided link.

## Contributing
Feel free to fork this repository and submit pull requests for improvements.

## License
This project is open-source and licensed under the MIT License.

