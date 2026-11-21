import os
import time
from jobspy import scrape_jobs
import requests

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

SEARCH_QUERIES = [
    # Java Backend
    "Java Developer Intern Sri Lanka",
    "Java Software Engineer Intern Sri Lanka",
    "Junior Java Developer Sri Lanka",
    "Spring Boot Developer Intern Sri Lanka",
    "Java Spring Boot Internship Sri Lanka",

    # Full Stack - Java + React
    "Java React Full Stack Intern Sri Lanka",
    "Spring Boot React Developer Intern Sri Lanka",
    "Full Stack Software Engineer Intern Sri Lanka",
    "Full Stack Developer Internship Sri Lanka",

    # React Frontend
    "React Developer Intern Sri Lanka",
    "Frontend Developer Intern React Sri Lanka",

    # Software Engineering
    "Software Engineer Intern Sri Lanka",
    "Software Engineering Internship Sri Lanka",
    "Associate Software Engineer Intern Sri Lanka",
    "Trainee Software Engineer Intern Sri Lanka",

    # Other relevant opportunities
    "Backend Developer Intern Sri Lanka",
    "Graduate Software Engineer Java Sri Lanka",
    "Software Developer Intern Sri Lanka",
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def job_search():
    print("🚀 Starting Job Radar for Lahiru...")
    
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}...")
        try:
            jobs = scrape_jobs(
                site_name=["linkedin", "indeed", "glassdoor"],
                search_term=query,
                location="Sri Lanka",
                results_wanted=3,
                hours_old=48,
            )
            
            if jobs.empty:
                time.sleep(3) # බ්लॉक වීම වළඳාගැනීමට පොඩි විරාමයක්
                continue

            for _, row in jobs.iterrows():
                title = row.get('title', 'N/A')
                company = row.get('company', 'N/A')
                job_url = row.get('job_url', '#')
                
                msg = f"🔥 *New Job Alert!*\n\n*Query:* {query}\n*Title:* {title}\n*Company:* {company}\n*Link:* {job_url}"
                send_telegram_message(msg)
                print(f"-> Sent: {title} at {company}")
                time.sleep(2) # මැසේජ් අතර පරතරය
                
        except Exception as e:
            print(f"Error for {query}: {e} (Cooling down...)")
            time.sleep(8) # 429 Error එකක් ආවොත් ටිකක් නතර වී සිටීම
            
    print("✅ Job Radar scan completed for this cycle.")

if __name__ == "__main__":
    job_search()
    # GitHub Actions වලදී infinite loop අවශ්‍ය නැත (Cron එකෙන් පාලනය වේ), 
    # නමුත් local එකේ run කරනවා නම් පහත loop එක තබා ගත හැක.