import database
import random
from datetime import datetime, timedelta
# Your list of netID applicants
applicants = ['ta0639', 'hd0216', 'abiehl', 'aa6162']

# Gigs data
gigs_data = [
    {
        "title": "Math Tutor for Algebra",
        "category": "teaching",
        "description": "Help students grasp algebra concepts, offering personalized, one-on-one tutoring sessions. Explain problem-solving techniques and provide practice exercises to boost their confidence.",
        "qualifications": "Strong math skills, previous tutoring experience, excellent communication skills, patience, ability to simplify complex concepts."
    },
    {
        "title": "Language Exchange Partner",
        "category": "teaching",
        "description": "Collaborate with fellow students to improve language fluency. Engage in conversations, correct pronunciation, and exchange cultural insights to make language learning an enriching experience.",
        "qualifications": "Bilingual in English and Spanish, patient, language enthusiast, availability for regular language exchange sessions."
    },
    {
        "title": "Research Assistant for Biology Project",
        "category": "research",
        "description": "Assist in a biology research project by collecting and analyzing data, conducting experiments, and contributing to research findings.",
        "qualifications": "Biology major with a strong foundation in research methods, laboratory experience, data analysis skills, ability to work independently and as part of a team."
    },
    {
        "title": "Market Research for Startup",
        "category": "research",
        "description": "Conduct in-depth market research to identify target audiences, assess competition, and gather valuable data for a startup's growth strategy.",
        "qualifications": "Strong analytical skills, knowledge of market research methodologies, ability to create surveys, analyze data, and provide actionable insights."
    },
    {
        "title": "Website Development for Student Club",
        "category": "technical",
        "description": "Create an engaging and user-friendly website for a student organization, ensuring it aligns with the club's branding and goals.",
        "qualifications": "Proficient in web development, HTML, CSS, JavaScript, ability to design user-friendly and responsive websites, experience in creating and maintaining web pages."
    },
    {
        "title": "Computer Repair Specialist",
        "category": "technical",
        "description": "Provide technical support to resolve computer problems, troubleshoot hardware issues, and offer solutions to enhance performance.",
        "qualifications": "Tech-savvy with hardware troubleshooting expertise, knowledge of common computer issues and their solutions, excellent problem-solving skills."
    },
    {
        "title": "Essay Editing and Proofreading",
        "category": "writing",
        "description": "Edit and proofread essays to ensure clarity, coherence, and grammatical accuracy. Offer constructive feedback to help improve the quality of written work.",
        "qualifications": "Strong writing skills, exceptional attention to detail, proficiency in grammar and style conventions, prior experience in proofreading and editing."
    },
    {
        "title": "Creative Writing Workshop Facilitator",
        "category": "writing",
        "description": "Lead interactive workshops that foster creativity and develop writing skills, providing constructive feedback and inspiration to workshop participants.",
        "qualifications": "Accomplished creative writer with published works, teaching experience in writing, ability to inspire and guide aspiring writers."
    },
    {
        "title": "Logo Design for Student Organization",
        "category": "graphic_design",
        "description": "Create a distinct and memorable logo that represents the identity and values of a student club, ensuring it stands out and resonates with the target audience.",
        "qualifications": "Graphic design skills, creativity, ability to translate concepts into unique visual designs, experience in logo design."
    },
    {
        "title": "Poster Design for Event",
        "category": "graphic_design",
        "description": "Design visually appealing posters that capture the essence of an upcoming event, ensuring that it attracts attendees and conveys key information effectively.",
        "qualifications": "Proficiency in design software (e.g., Adobe Creative Suite), experience in creating eye-catching posters, ability to effectively communicate event details visually."
    },
    {
        "title": "Graduation Photography",
        "category": "photography_film",
        "description": "Capture memorable and high-quality photographs during graduation ceremonies, preserving the special moments of fellow students as they mark this significant milestone.",
        "qualifications": "Photography skills, access to professional camera equipment, creative eye, ability to capture candid moments."
    },
    {
        "title": "Video Editing for Short Film",
        "category": "photography_film",
        "description": "Edit raw footage to create a compelling short film, refining the narrative and visual elements to convey a powerful message or story effectively.",
        "qualifications": "Video editing skills, creativity, proficiency in video editing software, ability to edit and enhance footage for storytelling purposes."
    },
    {
        "title": "Event Planning for Charity Fundraiser",
        "category": "events",
        "description": "Plan, organize, and execute a charity fundraising event, from concept development to logistics and promotion, ensuring its success and positive impact on the cause.",
        "qualifications": "Event planning experience, excellent organizational and project management skills, creativity, attention to detail, ability to coordinate various event elements."
    },
    {
        "title": "DJ for Student Party",
        "category": "events",
        "description": "Provide energetic and crowd-pleasing DJ services for a student party, creating a vibrant and memorable atmosphere with music that resonates with the audience.",
        "qualifications": "DJ skills, music knowledge, experience in creating playlists that cater to diverse musical tastes, proficiency in using DJ equipment."
    },
    {
        "title": "Social Media Manager for Club Promotion",
        "category": "marketing",
        "description": "Manage social media accounts to promote a student club, creating engaging content, tracking performance, and implementing strategies to boost visibility and engagement.",
        "qualifications": "Social media expertise, content creation, familiarity with social media analytics, ability to strategize and execute effective campaigns."
    },
    {
        "title": "Marketing Strategy Consultant for Startup",
        "category": "marketing",
        "description": "Collaborate with a startup to develop a comprehensive marketing strategy, including market analysis, target audience identification, and tactics to gain a competitive edge.",
        "qualifications": "Marketing knowledge, strategic thinking, experience in developing marketing strategies for startups, market analysis skills."
    },
    {
        "title": "Personal Assistant for Busy Student",
        "category": "administrative",
        "description": "Provide comprehensive personal assistant services to a busy student, managing their schedule, handling emails, and running errands to help streamline their daily life.",
        "qualifications": "Organizational skills, time management, ability to handle scheduling, emails, and errands efficiently, discretion with confidential tasks."
    },
    {
        "title": "Data Entry for Research Project",
        "category": "administrative",
        "description": "Accurately input data into a research project's database, ensuring data integrity and providing crucial support to ongoing research efforts.",
        "qualifications": "Exceptional attention to detail, data entry experience, proficiency in data management software, ability to maintain data accuracy."
    },
    {
        "title": "Community Cleanup Volunteer",
        "category": "volunteer",
        "description": "Volunteer your time to engage in community cleanup efforts, contributing to a cleaner and healthier local environment.",
        "qualifications": "Enthusiastic, environmentally conscious, willingness to participate in outdoor cleanup activities, dedication to making a positive impact on the community."
    },
    {
        "title": "Mentor for High School Students",
        "category": "volunteer",
        "description": "Serve as a mentor to high school students, providing guidance and support to help them navigate academic and personal challenges, and encouraging their personal growth and success.",
        "qualifications": "Patience, mentoring skills, willingness to offer guidance, strong communication skills, dedication to empowering and inspiring high school students."
    },
    {
        "title": "Content Creator for Social Media",
        "category": "other",
        "description": "Create engaging content for social media platforms to boost engagement and reach the target audience. Develop creative posts, images, and videos to showcase the brand's personality.",
        "qualifications": "Social media expertise, content creation skills, knowledge of social media trends, creativity, ability to plan and execute content strategy."
    },
    {
        "title": "Virtual Assistant for Online Business",
        "category": "other",
        "description": "Provide virtual assistance to support the daily operations of an online business. Manage emails, appointments, data entry, and administrative tasks efficiently.",
        "qualifications": "Organizational skills, time management, proficiency in office software, ability to handle administrative tasks remotely."
    },
    {
        "title": "Graphic Design for Event Flyer",
        "category": "other",
        "description": "Design eye-catching event flyers for various occasions. Create visually appealing graphics and layouts to attract attendees and convey event details effectively.",
        "qualifications": "Graphic design skills, proficiency in design software, experience in creating event flyers."
    },
    {
        "title": "Virtual Yoga Instructor",
        "category": "other",
        "description": "Lead virtual yoga sessions to help participants improve their flexibility and mental well-being. Offer guided yoga practice to suit different levels of expertise.",
        "qualifications": "Certified yoga instructor, ability to lead virtual yoga sessions, knowledge of different yoga styles, excellent communication skills."
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
        startfrom = today + timedelta(days=random.randint(1, 7))  # Random date within a week
        until = startfrom + timedelta(days=random.randint(1, 7))  # Random date within a week
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
