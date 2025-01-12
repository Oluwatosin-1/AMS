Skillsquared Affiliate Management System
Skillsquared Affiliate Management System (AMS) is a robust platform for managing affiliates, tracking referrals, processing payments, and enhancing affiliate engagement through training programs. It is designed to empower businesses and affiliates to collaborate effectively while maximizing conversions and revenue.
 
Features
1. User Management
•	Custom User Model:
o	Admins and affiliates are categorized using a custom user model (CustomUser).
o	Affiliates can register and manage their accounts independently.
•	Admin and Affiliate Dashboards:
o	Admin dashboard for managing affiliates, products, and analytics.
o	Affiliate dashboard for tracking earnings, referrals, and training progress.
 
2. Referral Tracking
•	Unique Referral Links:
o	Auto-generated unique referral links for each affiliate and product pairing.
o	Links include query parameters for accurate tracking (e.g., ?ref=AFF123).
•	Cookie-Based Tracking:
o	Referral activity tracked via browser cookies (30-day lifespan).
o	Ensures proper commission allocation for referred purchases.
•	Client Genealogy:
o	Comprehensive tracking of referral relationships and affiliate hierarchies.
 
3. Product Management
•	Admin Features:
o	Add, edit, and delete products with descriptions, images, and prices.
o	Assign unique referral links to each affiliate for every product.
•	Affiliate Features:
o	Access product-specific referral links in the affiliate dashboard.
o	Monitor product performance and commission earnings.
 
4. Training and Certification
•	Online Training Modules:
o	Modules covering marketing strategies, referral techniques, and performance tips.
o	Affiliates track their progress and complete courses at their own pace.
•	Certification:
o	Affiliates earn certifications upon completing training, unlocking higher commissions.
•	Admin Features:
o	Create and manage training modules.
 
5. Affiliate Dashboard
•	Performance Metrics:
o	Track total earnings, pending commissions, conversion rates, and clicks.
•	Referral List:
o	View referred clients and their purchase statuses (e.g., "Completed", "Pending").
•	Revenue Insights:
o	Breakdown of commission earnings by product or period.
o	Lifetime value of referred clients.
 
6. Payments
•	Payout Management:
o	Payouts triggered monthly or upon reaching a predefined threshold.
o	Affiliates select payment methods (e.g., PayPal, bank transfer).
•	Payment History:
o	Affiliates can view detailed payment records, including status and dates.
•	Admin Features:
o	Manage and process affiliate payouts through the admin dashboard.
 
7. Admin Dashboard
•	Affiliate Management:
o	Add, edit, or remove affiliates.
o	Adjust commission rates and monitor affiliate performance.
•	Referral Analytics:
o	Generate reports on affiliate performance, including referral numbers, conversions, and earnings.
•	Client Genealogy:
o	View and manage referral hierarchies.
 
8. Engagement and Retention
•	Leaderboards:
o	Competitive leaderboards for top-performing affiliates.
•	Performance-Based Rewards:
o	Bonuses or exclusive offers for high-achieving affiliates.
•	Regular Communication:
o	Automated newsletters and marketing tips to keep affiliates engaged.
 
9. Marketing Resources
•	Promotional Materials:
o	Access to banners, email templates, and social media assets.
•	Sales Kits:
o	Downloadable pitch decks and product sheets for affiliates.
 
Technology Stack
•	Backend: Django (Python)
•	Frontend: HTML, CSS, Bootstrap/Tailwind
•	Database: PostgreSQL/MySQL (configurable)
•	Middleware: Referral tracking via custom middleware
•	APIs: Django REST Framework (optional)
 
Setup Instructions
1. Prerequisites
•	Python 3.10+
•	Virtual Environment (e.g., venv or virtualenv)
•	PostgreSQL/MySQL database setup
2. Installation
1.	Clone the repository:
bash
Copy code
git clone https://github.com/your-username/skillsquared-affiliate-system.git
cd skillsquared-affiliate-system
2.	Set up a virtual environment:
bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
3.	Install dependencies:
bash
Copy code
pip install -r requirements.txt
4.	Configure the database in settings.py:
python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
5.	Apply migrations:
bash
Copy code
python manage.py makemigrations
python manage.py migrate
6.	Create a superuser:
bash
Copy code
python manage.py createsuperuser
7.	Run the development server:
bash
Copy code
python manage.py runserver
8.	Access the application at http://127.0.0.1:8000/.
 
Folder Structure
perl
Copy code
skillsquared-affiliate-system/
├── affiliates/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
├── products/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
├── payments/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── training/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── referrals/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── templates/
│   ├── affiliates/
│   ├── products/
│   ├── payments/
│   ├── training/
│   ├── referrals/
└── manage.py
 
Future Enhancements
•	Add multi-level marketing (MLM) features.
•	Implement advanced analytics dashboards.
•	Integrate third-party payment gateways (e.g., Stripe, Razorpay).
•	Enable tiered commissions and bonuses.

![image](https://github.com/user-attachments/assets/00b70375-c859-4aa0-a180-405bba4c4f79)
