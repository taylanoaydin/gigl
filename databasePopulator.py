import database
import random
from datetime import datetime, timedelta
# Your list of netID applicants
applicants = ['ta0639', 'hd0216', 'abiehl', 'aa6162']

# Gigs data
gigs_data = [
    {
        "title": "Social Media Campaign Coordinator",
        "category": "marketing",
        "description": "Develop and manage a social media campaign for a new product launch. Create engaging content, analyze engagement data, and adapt strategies to maximize reach and impact.",
        "qualifications": "Experience in social media management, strong understanding of analytics, creative thinking, excellent communication skills."
    },
    {
        "title": "Java Programming Tutor",
        "category": "teaching",
        "description": "Provide one-on-one Java programming tutoring sessions. Assist students in understanding core concepts, debugging code, and developing small projects.",
        "qualifications": "Proficient in Java, experience in teaching or tutoring, patient, good at explaining complex concepts in a simple manner."
    },
    {
        "title": "Undergraduate Research Assistant in Chemistry",
        "category": "research",
        "description": "Support a research team in the Chemistry department. Assist with laboratory experiments, data collection, and analysis. Help in preparing research papers.",
        "qualifications": "Majoring in Chemistry, lab experience, detail-oriented, good analytical skills."
    },
    {
        "title": "iOS App Developer for Campus Project",
        "category": "technical",
        "description": "Develop an iOS application for a campus initiative. Work with a team to design, code, and test the app. Ensure app usability and aesthetic appeal.",
        "qualifications": "Proficient in Swift and iOS development, experience with UI/UX design, teamwork skills."
    },
    {
        "title": "Freelance Journalist for University Magazine",
        "category": "writing",
        "description": "Write articles for the university magazine covering various campus events, student life, and local news. Conduct interviews and research to create compelling stories.",
        "qualifications": "Strong writing skills, ability to conduct interviews, research skills, ability to meet deadlines."
    },
    {
        "title": "Graphic Designer for Online Branding",
        "category": "graphic_design",
        "description": "Create visual content for an online brand, including social media graphics, website banners, and promotional materials. Work closely with the marketing team to maintain brand consistency.",
        "qualifications": "Proficient in Adobe Creative Suite, creative flair, understanding of branding and marketing."
    },
    {
        "title": "Documentary Photographer",
        "category": "photography_film",
        "description": "Photograph events and day-to-day activities on campus for a documentary project. Capture candid and staged shots, edit photos, and assist in curating a photo exhibition.",
        "qualifications": "Photography skills, experience with photo editing software, creative eye, attention to detail."
    },
    {
        "title": "Campus Event Organizer",
        "category": "events",
        "description": "Plan and execute campus events, including coordinating with vendors, managing logistics, promoting the event, and overseeing event proceedings.",
        "qualifications": "Strong organizational skills, experience in event planning, good communication, ability to handle multiple tasks."
    },
    {
        "title": "Digital Marketing Analyst for Startup",
        "category": "marketing",
        "description": "Analyze digital marketing campaigns for a startup. Use analytics tools to track performance, generate reports, and provide insights for optimization.",
        "qualifications": "Experience with digital marketing analytics, strong analytical skills, proficiency in data analysis tools."
    },
    {
        "title": "Administrative Support Intern",
        "category": "administrative",
        "description": "Provide administrative support in an office setting. Manage schedules, handle communications, and assist with various administrative tasks.",
        "qualifications": "Organizational skills, proficiency in office software, excellent communication skills, ability to multitask."
    },
    {
        "title": "Environmental Awareness Campaign Volunteer",
        "category": "volunteer",
        "description": "Participate in an environmental awareness campaign. Help organize events, disseminate information, and engage with the community to promote sustainability.",
        "qualifications": "Passionate about environmental issues, good communication skills, enthusiastic, team player."
    },
    {
        "title": "E-commerce Website Manager",
        "category": "other",
        "description": "Manage and maintain an e-commerce website. Ensure smooth operation, update product listings, and work on SEO to improve site visibility.",
        "qualifications": "Experience with e-commerce platforms, knowledge of SEO, strong technical and problem-solving skills."
    },
    {
        "title": "Virtual Event Coordinator",
        "category": "other",
        "description": "Coordinate and manage virtual events. Handle technology setup, coordinate with speakers, and ensure smooth running of online events.",
        "qualifications": "Experience with virtual event platforms, good organizational skills, technical proficiency, strong communication skills."
    }
]

random.shuffle(gigs_data)

# Function to create gigs for each netID applicant
def create_gigs_for_applicant(applicant_netID, gigs_data, num_gigs):
    applied_gigs = set()
    today = datetime.now().date()
    for _ in range(num_gigs):
        gig_data = gigs_data.pop()  # Pop the last gig from the randomized list
        title = gig_data["title"]
        category = gig_data["category"]
        description = gig_data["description"]
        qualifications = gig_data["qualifications"]
        
        # Define the dates
        startfrom = today + timedelta(days=random.randint(4, 14))  # Random date within a week
        until = startfrom + timedelta(days=random.randint(15, 200))  # Random date within a week
        posted = today
        
        gigID = database.create_gig(applicant_netID, title, category, description, qualifications, startfrom, until, posted)
        if gigID == -1:
            print(f"Failed to create a gig for {applicant_netID}")
        else:
            applied_gigs.add(gigID)
            print(f"Created gig with ID {gigID} for {applicant_netID}")
    
    return applied_gigs

# Create gigs for each netID applicant with 5 job openings each
for applicant_netID in applicants:
    gigs_data_copy = list(gigs_data)
    applied_gigs = create_gigs_for_applicant(applicant_netID, gigs_data_copy, 6)
    
    # Return the gigs back to gigs_data for other applicants
    gigs_data.extend([gig for gig in gigs_data_copy if gig["title"] not in applied_gigs])
