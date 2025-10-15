# Multi-Tenant Insurance Management System

A comprehensive, multi-tenant insurance platform built with Django REST Framework and PostgreSQL, featuring complete claim lifecycle management, policy administration, and role-based access control. Each insurance company operates in its own isolated tenant environment with secure data separation.

## 🚀 What Problems Does It Solve?

### For Insurance Companies
- **Multi-Tenant Architecture**: Complete data isolation between different insurance companies
- **Scalable Operations**: Handle multiple insurance companies on a single platform
- **Secure Data Management**: Each company's data is completely separated and secure
- **Customizable Workflows**: Flexible claim processing workflows tailored to each company's needs

### For Claims Processing Teams
- **Complete Claim Lifecycle**: From initial report to final settlement with status tracking
- **Role-Based Access Control**: Different permissions for call center, adjusters, managers, and admins
- **Document Management**: Secure file upload and management for claim supporting documents
- **Audit Trail**: Complete history of claim notes, status changes, and assignments

### For Policy Management
- **Policy Administration**: Create, update, and manage insurance policies
- **Policy Renewal**: Streamlined policy renewal process with date validation
- **Search & Discovery**: Advanced search across policy numbers, holders, and contact information
- **Coverage Tracking**: Monitor policy coverage amounts, premiums, and validity periods

### For System Administrators
- **Tenant Onboarding**: Streamlined registration and approval process for new insurance companies
- **Global Administration**: Platform-wide management and oversight capabilities
- **User Management**: Create and manage users across different roles and permissions
- **Report Generation**: Comprehensive reporting system for business intelligence

## ✨ Key Features

### 🏢 Multi-Tenant Architecture
- **Schema Isolation**: Each insurance company operates in its own database schema
- **Domain-Based Routing**: Custom domains for each tenant (e.g., abcinsurance.com)
- **Data Security**: Complete separation of data between tenants
- **Scalable Design**: Support for unlimited insurance companies

### 📋 Claims Management System
- **Complete Lifecycle**: 10-stage claim workflow from reported to closed
- **Status Transitions**: Validated state machine for claim status changes
- **Assignment System**: Assign claims to specific adjusters and managers
- **Document Upload**: Support for multiple document types (photos, reports, estimates, etc.)
- **Internal Notes**: Secure internal communication system for claim processing

### 👥 Role-Based Access Control
- **Call Center Agents**: Create and manage initial claim reports
- **Claims Adjusters**: Investigate and process claims
- **Senior Adjusters**: Advanced claim processing and approval
- **Claims Managers**: Final approval authority and oversight
- **Tenant Admins**: Complete tenant management capabilities
- **Global Admins**: Platform-wide administration

### 📄 Policy Management
- **Policy Types**: Support for auto, home, life, health, business, travel insurance
- **Coverage Tracking**: Monitor coverage amounts and premium payments
- **Renewal System**: Automated policy renewal with date validation
- **Search Functionality**: Advanced search across policy data

### 🔐 Security & Authentication
- **JWT Authentication**: Secure token-based authentication system
- **Permission Classes**: Granular permission control for each endpoint
- **Password Management**: Secure password update and reset functionality
- **Tenant Context**: Automatic tenant isolation in all operations

### 📊 Reporting System
- **Custom Reports**: Generate reports for business intelligence
- **Tenant-Specific**: Reports scoped to individual insurance companies
- **User Tracking**: Track report creation and modification history

## 🏗️ Architecture

### Backend (Django REST Framework)
- **Django 5.2.6**: Modern Python web framework with multi-tenant support
- **Django REST Framework**: Powerful API development with comprehensive serializers
- **django-tenants**: Multi-tenant architecture with schema isolation
- **JWT Authentication**: Secure authentication with SimpleJWT
- **PostgreSQL**: Robust database with schema-based multi-tenancy
- **CORS Support**: Cross-origin resource sharing for frontend integration

### Multi-Tenant Design
- **Public Schema**: Shared data for tenant management and registration
- **Tenant Schemas**: Isolated schemas for each insurance company
- **Domain Routing**: Automatic tenant resolution based on domain
- **Schema Context**: Secure context switching between tenants

### Database Models
- **InsuranceCompany**: Tenant model with company information
- **User**: Multi-tenant user model with role-based permissions
- **Policy**: Insurance policy management with coverage tracking
- **Claim**: Comprehensive claim model with status workflow
- **ClaimNote**: Internal communication system for claims
- **ClaimDocument**: File management for claim supporting documents
- **Report**: Business intelligence and reporting system

## 🛠️ Technology Stack

### Backend Dependencies
```
Django==5.2.6
djangorestframework==3.16.1
django-cors-headers==4.9.0
djangorestframework-simplejwt==5.5.1
django-tenants==3.9.0
django-filter==25.1
psycopg2-binary==2.9.10
Pillow==11.3.0
python-dotenv==1.1.1
```

### Database
- **PostgreSQL**: Primary database with schema-based multi-tenancy
- **Schema Isolation**: Complete data separation between tenants
- **Migrations**: Tenant-aware database migrations

### Infrastructure
- **Multi-Domain Support**: Custom domain routing for each tenant
- **File Storage**: Secure file upload and management
- **Email Integration**: SMTP support for notifications (ready for implementation)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Virtual environment (recommended)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mlt_tenants_insurance
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Database Configuration**
   Create a PostgreSQL database and update settings:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django_tenants.postgresql_backend',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Environment Variables**
   Create a `.env` file in the backend directory:
   ```env
   SECRET_KEY=your-django-secret-key
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   DEBUG=True
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate_schemas --shared
   python manage.py migrate_schemas
   python manage.py createadmin
   ```

### Running the Application

#### Development Mode

1. **Start Django Backend**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Access the Application**
   - Main site: `http://localhost:8000/`
   - Admin panel: `http://localhost:8000/admin/`

#### Creating a New Tenant

1. **Register New Insurance Company**
   ```bash
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "company_name": "ABC Insurance Co.",
       "business_type": "auto",
       "company_phone": "+1234567890",
       "contact_email": "contact@abcinsurance.com",
       "company_address": "123 Main St, City, State",
       "requested_domain": "abcinsurance.localhost",
       "admin_email": "admin@abcinsurance.com",
       "admin_username": "admin",
       "admin_password": "securepassword"
     }'
   ```

2. **Approve Registration** (Admin only)
   ```bash
   curl -X POST http://localhost:8000/administration/registration-requests/1/approve/ \
     -H "Authorization: Bearer your-jwt-token"
   ```

3. **Access Tenant Site**
   - Tenant site: `http://abcinsurance.localhost:8000/`

## 📚 API Documentation

### Authentication Endpoints
- `POST /users/login/` - User authentication with JWT tokens
- `POST /users/add-user/` - Register new user in tenant
- `POST /users/update-email/` - Update user email address
- `POST /users/update-password/` - Update user password
- `GET /users/generate-reset-token/` - Generate password reset code

### Policy Management
- `GET /policies/` - List all policies
- `POST /policies/` - Create new policy
- `GET /policies/{id}/` - Get specific policy
- `PUT /policies/{id}/` - Update policy
- `DELETE /policies/{id}/` - Delete policy
- `PUT /policies/{id}/renew/` - Renew policy
- `GET /policies/search/?key_word={keyword}` - Search policies

### Claims Management
- `GET /policy/{id}/claims/` - List claims for policy
- `POST /policy/{id}/claims/` - Create new claim
- `GET /policy/{id}/claims/{id}/` - Get specific claim
- `PUT /policy/{id}/claims/{id}/` - Update claim
- `DELETE /policy/{id}/claims/{id}/` - Delete claim
- `POST /claims/{id}/assign/?user_id={uuid}` - Assign claim to user
- `PUT /claims/{id}/update-status/?new_status={status}` - Update claim status

### Claim Notes & Documents
- `POST /claims/{id}/add-note/` - Add note to claim
- `GET /notes/{id}/` - Get claim note
- `PUT /notes/{id}/` - Update claim note
- `DELETE /notes/{id}/` - Delete claim note
- `POST /claims/{id}/add-document/` - Upload document to claim
- `GET /documents/{id}/` - Get claim document
- `PUT /documents/{id}/` - Update document metadata
- `DELETE /documents/{id}/` - Delete claim document

### User Management
- `GET /users/{id}/` - Get user profile
- `GET /users/{id}/claims/` - Get user's assigned claims
- `GET /users/?role={role}` - Get users by role

### Reports
- `GET /reports/` - List all reports
- `POST /reports/` - Create new report
- `GET /reports/{id}/` - Get specific report
- `PUT /reports/{id}/` - Update report
- `DELETE /reports/{id}/` - Delete report

### Administration (Global)
- `GET /administration/registration-requests/` - Get pending registrations
- `POST /administration/registration-requests/{id}/approve/` - Approve registration
- `DELETE /administration/registration-requests/{id}/reject/` - Reject registration
- `GET /administration/add-global-admin/` - Add global administrator

### Tenant Registration
- `POST /register/` - Submit registration request

## 🔧 Configuration

### Django Settings
Key settings in `backend/mlt_ins/settings.py`:
- Multi-tenant configuration with django-tenants
- JWT token lifetime configuration
- CORS settings for frontend integration
- Media file handling for document uploads
- Database configuration for PostgreSQL

### Tenant Configuration
- **Domain Management**: Automatic domain-based tenant resolution
- **Schema Creation**: Automatic schema creation for new tenants
- **Permission Classes**: Custom permission classes for role-based access

### Claim Status Workflow
```
reported → assigned → under_review → investigation → 
documents_requested → waiting_approval → approved/denied → 
payment_processing → paid → closed
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### API Testing
Use the provided endpoints with tools like:
- Postman
- curl
- Django REST Framework browsable API

## 📦 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure production PostgreSQL database
- [ ] Set up domain routing for tenants
- [ ] Configure static file serving
- [ ] Set up SSL certificates for all tenant domains
- [ ] Configure email SMTP settings
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy for multi-tenant data

### Multi-Domain Setup
Each tenant requires:
- Custom domain configuration
- SSL certificate setup
- DNS configuration
- Database schema isolation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django Tenants for multi-tenant architecture
- Django REST Framework community
- PostgreSQL for robust database support
- All contributors and users

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the UML diagrams in `/backend/uml/`

## 🎯 Business Value

### For Insurance Companies
- **Cost Reduction**: Shared platform infrastructure reduces operational costs
- **Faster Time-to-Market**: Quick onboarding and setup process
- **Scalability**: Handle growth without infrastructure concerns
- **Compliance**: Built-in audit trails and security features

### For Platform Operators
- **Recurring Revenue**: Subscription-based model for insurance companies
- **Scalable Business**: Add unlimited insurance companies
- **Operational Efficiency**: Centralized management and monitoring
- **Market Expansion**: Serve multiple insurance markets simultaneously

---

**Multi-Tenant Insurance Management System** - Secure, Scalable, Professional 🚀
