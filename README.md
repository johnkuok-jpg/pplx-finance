# Invoice Banking Information Updater

A simple web application to update banking information on Stripe-formatted invoice PDFs.

## Features

- 🎯 Drag and drop PDF upload
- 📝 Easy form to enter new banking details
- 🔄 One-click invoice modification
- 📥 Instant download of modified PDF
- 🔒 All processing happens locally (no server storage)

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run invoice_modifier_app.py
```

3. Open your browser to `http://localhost:8501`

## Deploying to Streamlit Cloud (Free)

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `invoice-modifier` or `pdf-banking-updater`
3. Make it public or private (your choice)

### Step 2: Upload Files to GitHub

Upload these files to your repository:
- `invoice_modifier_app.py`
- `requirements.txt`
- `README.md` (optional)

You can do this through:
- GitHub's web interface (drag and drop)
- Git command line:
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and the main file (`invoice_modifier_app.py`)
5. Click "Deploy"

**That's it!** Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

Streamlit Cloud is completely free for public repositories!

## Alternative Deployment Options

### Heroku (Free Tier)

1. Create a `Procfile`:
```
web: streamlit run invoice_modifier_app.py --server.port=$PORT
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway (Free Tier)

1. Connect your GitHub repo to Railway
2. Railway auto-detects Streamlit apps
3. Deploy with one click

### Docker (Self-hosted)

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "invoice_modifier_app.py"]
```

2. Build and run:
```bash
docker build -t invoice-modifier .
docker run -p 8501:8501 invoice-modifier
```

## Usage

1. Open the web app
2. Drag and drop your Stripe invoice PDF
3. Fill in the new banking information:
   - Bank Name
   - Account Name
   - Account Type
   - ACH Routing/ABA
   - Account Number
   - Swift/IBAN
   - Reference
4. Click "Update Invoice"
5. Download the modified PDF

## Security & Privacy

- All PDF processing happens in your browser session
- No files are stored on any server
- No data is transmitted or saved
- All processing is done in-memory

## How It Works

The app:
1. Reads the uploaded PDF
2. Locates the "Bank name" section in the banking details
3. Removes all text from that line to the bottom of the page
4. Adds the new banking information in the same format
5. Returns the modified PDF for download

## Supported Invoice Formats

Currently optimized for:
- Stripe invoice PDFs
- PDFs with a "Bank name" label in the banking section
- Standard letter-size (8.5" x 11") PDFs

## Troubleshooting

**"Could not find 'Bank name' in the PDF"**
- Ensure your PDF has a banking section with "Bank name" text
- The PDF must be in a format similar to Stripe invoices

**Text not aligning properly**
- The app is optimized for Stripe's standard invoice format
- Custom invoice templates may require code adjustments

## Contributing

Feel free to fork and improve this project!

## License

MIT License - feel free to use for personal or commercial purposes.

## Built With

- [Streamlit](https://streamlit.io) - Web framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF manipulation library
