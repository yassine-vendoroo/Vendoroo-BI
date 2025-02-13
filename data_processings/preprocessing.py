import re
import unicodedata
from bs4 import BeautifulSoup
import json

def normalize_text(text):
    """
    Normalize unicode text to NFKD form.
    
    Args:
        text (str): The text to normalize.
    
    Returns:
        str: The normalized text.
    """
    return unicodedata.normalize('NFKD', text)

def convert_html_to_text(html):
    """
    Convert HTML content to plain text and extract image sources.
    
    Args:
        html (str): The HTML content to convert.
    
    Returns:
        str: The plain text with image sources appended.
    """
    if not html:
        return ''
    
    soup = BeautifulSoup(html, features="html.parser")

    # Remove all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text('\n')

    # Break into lines and remove leading and trailing space on each
    lines = (line for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Extract image sources
    images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    images_text = " Images: " + ', '.join(images) if images else ""
    
    return text + images_text

def strip_html_tags(text):
    """
    Remove HTML tags from text.
    
    Args:
        text (str): The text with HTML tags.
    
    Returns:
        str: The text without HTML tags.
    """
    soup = BeautifulSoup(text, 'html.parser')
    plain_text = soup.get_text()
    clean = re.compile('<.*?>')
    return re.sub(clean, '', plain_text)

def extract_email_content(html_string):
    """
    Extract main content and thread content from an email HTML string.
    
    Args:
        html_string (str): The HTML string of the email.
    
    Returns:
        tuple: A tuple containing the main content and thread content.
    """
    soup = BeautifulSoup(html_string, 'html.parser')
    thread_content = ""
    try:
        selectors = [
            ('.gmail_quote', 'gmail'),
            ('.yahoo_quoted', 'yahoo'),
            ('.custom-quote', 'custom'),
            ("[style*='border:none;border-top:solid #E1E1E1 1.0pt;padding:3.0pt 0in 0in 0in']", 'other')
        ]
        for css_selector, type_ in selectors:
            content = soup.select_one(css_selector)
            if content:
                if type_ == 'custom':
                    next_sibling = content.find_next_sibling()
                    while next_sibling:
                        if next_sibling.name:
                            content.append(next_sibling.extract())
                        else:
                            next_sibling.decompose()
                        next_sibling = content.find_next_sibling()
                thread_content += strip_html_tags(str(content))
                content.decompose()
        other_email_thread_content = soup.find(attrs={"style": re.compile("margin: 0 0 20px 0;")})
        if other_email_thread_content and other_email_thread_content.name == 'blockquote':
            regex = re.compile(r"On (Wed|Mon|Tue|Thu|Fri|Sat|Sun),")
            if any(regex.search(child.get_text()) for child in other_email_thread_content.find_all(text=True)):
                thread_content += strip_html_tags(str(other_email_thread_content))
                other_email_thread_content.decompose()
        new_main_text = strip_html_tags(str(soup))
        return new_main_text, thread_content
    except Exception as e:
        return "", ""

def extract_reported_issue(text):
    """
    Extract the reported issue from the text.
    
    Args:
        text (str): The text containing the reported issue.
    
    Returns:
        str: The extracted reported issue.
    """
    regex = r"^(?:.*)reported issue:?(.*)(?:address|work location|Unit is vacant|resident contact|address:|Permission to enter)"
    r = re.findall(regex, text, flags=re.S + re.IGNORECASE)
    
    if len(r) > 0:
        text = r[0]
       
    regex = r"^(.*)(?:address|work location|Unit is vacant|resident contact|address:|Permission to enter)"
    r = re.findall(regex, text, flags=re.S + re.IGNORECASE)
    
    if len(r) > 0:
        text = r[0]
    
    return text.strip()

def preprocess_scope_of_work(sow):
    """
    Preprocess the scope of work (SOW) by converting HTML to text and normalizing it.
    
    Args:
        sow (str): The scope of work in HTML format.
    
    Returns:
        str: The preprocessed scope of work.
    """
    cleaned_sow = convert_html_to_text(sow)
    return normalize_text(cleaned_sow).strip()

def convert_transcripts_to_text(transcripts):
    """
    Convert call transcripts to plain text.
    
    Args:
        transcripts (list): The list of transcript entries.
    
    Returns:
        str: The plain text of the transcripts.
    """
    text = ""
    for entry in transcripts:
        speaker = entry["speaker"]
        start_time = entry["startTime"]
        end_time = entry["endTime"]
        message = entry["text"]
        text += f"{speaker}: {message}\n"
    return text

def preprocess_call_transcripts(call_transcripts):
    """
    Preprocess call transcripts by converting them to plain text.
    
    Args:
        call_transcripts (str): The JSON string of call transcripts.
    
    Returns:
        str: The preprocessed call transcripts.
    """
    if call_transcripts:
        call_data = json.loads(call_transcripts)
    else:
        call_data = []
    call = convert_transcripts_to_text(call_data)
    return call.strip()

def preprocess_sms_message(sms):
    """
    Preprocess SMS message by stripping leading and trailing whitespace.
    
    Args:
        sms (str): The SMS message.
    
    Returns:
        str: The preprocessed SMS message.
    """
    return sms.strip()

def preprocess_email_content(email):
    """
    Preprocess email content by extracting the main content and stripping whitespace.
    
    Args:
        email (str): The email content in HTML format.
    
    Returns:
        str: The preprocessed email content.
    """
    main_content, _ = extract_email_content(email)
    return main_content.strip()

def preprocess_status_update(status_update):
    """
    Preprocess status update by extracting the reported issue.
    
    Args:
        status_update (str): The status update text.
    
    Returns:
        str: The preprocessed status update text.
    """
    try:
        status_data = json.loads(status_update)
        title = status_data.get('title', '') 
        status = status_data.get('status', '')
        status_update = f"New status: {status}\n" if status else ""
        summary = status_data.get('summary', '')
        status_text = f"{status_update}"
        status_text += f"{title}: " if title else ""
        status_text += f"{summary}"
    except json.JSONDecodeError:
        status_text = status_update
    return status_text