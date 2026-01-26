# GigGrid Generator

## Overview

GigGrid Generator is a small tool to help you quickly take a CSV of gigs and generate a nicely formatted HTML grid **as well as copy the content to your clipboard** for easy pasting into email templates. It’s designed to be simple: you select your CSV, run the app, and your data is ready to use.

---

## 🖥 Running the App

### Mac

- Download and unzip the folder inside `dist/MacOS/`.  
- Double-click the `.app` to launch.  

**Note:** macOS may warn that the app is from an “unidentified developer.” You can bypass this by:  

- Right-clicking the app → Open → Open again when prompted.

### Windows

- Download and run the executable from `dist/Windows/`.  

**Note:** If Windows warns about an unknown publisher, click **More info → Run anyway**.

---

## ⚡ How It Works

1. Open the app.  
2. Load your CSV file of events.  
3. The app will:  
   - Copy the formatted event info to your clipboard.  
   - Write out an HTML file containing the events, including images and links.  
4. Paste the clipboard contents directly into email templates.  
5. The HTML is also written out to a document and can be used at a later date.

---

## CSV Format

To ensure the app works correctly, your CSV file must have the following columns, in this order:

| Column        | Description                                                                                  |
|---------------|----------------------------------------------------------------------------------------------|
| **Artist Name** | Full name of the artist or band. If the name contains a comma, wrap it in double quotes.    |
| **Event Date**  | Day of the week, numeric day, and month (e.g., `Friday 5th December`).                       |
| **Start Time**  | Event start time in 24-hour format (e.g., `19:30`).                                         |
| **Ticket Info** | Ticket price and purchase notes (e.g., `£10 in advance`).                                     |
| **Event Link**  | URL to the event page on the venue website.                                                  |
| **Image URL**   | Direct URL to the event image, used for display in the HTML output.                           |

**Notes:**

- The first row **must be the header**.  
- No extra columns or missing headers — the app relies on this exact schema.
- Columns must remain in this order.
- The script will:  
  - Copy all event info to the clipboard for easy pasting into social media or emails.  
  - Generate an HTML file of the events for web embedding.

---

That’s it! With the CSV in the correct format, the app handles everything else: formatting, HTML output, and clipboard copying — saving you time putting together the mailer.
