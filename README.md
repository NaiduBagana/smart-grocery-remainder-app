# Smart Grocery Reminder App 🛒

A serverless web application built on AWS that helps users track grocery items and receive automated email reminders before items expire. The app leverages AWS services including Lambda, DynamoDB, SES, and EventBridge to provide a seamless experience for managing grocery expiration dates.

**🌐 Live Demo**: [http://grocery-reminder-app-stn.s3-website-us-east-1.amazonaws.com](http://grocery-reminder-app-stn.s3-website-us-east-1.amazonaws.com)

## 📋 Project Overview

The Smart Grocery Reminder App is designed to solve the common problem of food waste by helping users keep track of their grocery items' expiration dates. Users can add items through a modern web interface, and the system automatically sends email reminders one day before items are set to expire.

**Key Technologies:**
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: AWS Lambda (Python & Node.js)
- **Database**: Amazon DynamoDB
- **Email Service**: Amazon SES
- **API**: Amazon API Gateway
- **Scheduling**: Amazon EventBridge
- **Hosting**: Amazon S3 (Static Website)

## ✨ Key Features

### 🎯 **Real-World Application**
- Reduces food waste by tracking expiration dates
- Sends proactive email notifications before items expire
- Modern, responsive web interface

### ⚡ **Event-Driven & Scheduled Architecture**
- Immediate email confirmation upon item addition
- Automated daily scanning for expiring items
- Serverless architecture with automatic scaling

### 🔧 **Separation of Concerns**
- Clean separation between frontend and backend
- RESTful API endpoints for data operations
- Modular Lambda functions for specific tasks

### 🔒 **Minimal IAM Configuration**
- Secure access patterns with least privilege principle
- CORS-enabled API for web access
- Protected email sending through SES

## 🏗️ Architecture Components

### **Amazon S3**
- **Purpose**: Hosts the static website (HTML, CSS, JS)
- **Configuration**: Static website hosting enabled
- **Role**: Serves the frontend application to users

### **AWS Lambda Functions**

#### 1. `saveGroceryItem.py`
- **Purpose**: Saves new grocery items and sends confirmation emails
- **Triggers**: HTTP POST via API Gateway
- **Actions**: 
  - Stores item data in DynamoDB
  - Sends immediate confirmation email via SES

#### 2. `getGroceryItems.py`
- **Purpose**: Retrieves all stored grocery items
- **Triggers**: HTTP GET via API Gateway
- **Actions**: Scans DynamoDB table and returns all items

#### 3. `sendExpiryReminders.py`
- **Purpose**: Sends expiration reminder emails
- **Triggers**: EventBridge schedule (daily)
- **Actions**: 
  - Scans for items expiring tomorrow
  - Sends reminder emails via SES

#### 4. `handleCorsOptions.js`
- **Purpose**: Handles CORS preflight requests
- **Triggers**: HTTP OPTIONS via API Gateway
- **Actions**: Returns appropriate CORS headers

### **Amazon DynamoDB**
- **Table Name**: `GroceryItems`
- **Schema**:
  - `userEmail` (String): User's email address
  - `itemName` (String): Name of the grocery item
  - `expiryDate` (String): Expiration date (YYYY-MM-DD format)

### **Amazon API Gateway**
- **Purpose**: Provides RESTful endpoints for the frontend
- **Endpoints**:
  - `POST /saveGroceryItem`: Add new grocery item
  - `GET /grocery-items`: Retrieve all items
  - `OPTIONS /*`: Handle CORS preflight

### **Amazon EventBridge**
- **Purpose**: Triggers daily expiration checks
- **Schedule**: Daily execution of reminder function
- **Target**: `sendExpiryReminders` Lambda function

### **Amazon SES**
- **Purpose**: Sends confirmation and reminder emails
- **Configuration**: Verified sender email required
- **Templates**: Plain text email notifications

## 🚀 Setup and Deployment

### Prerequisites
- AWS Account with appropriate permissions
- AWS CLI configured
- Verified email address in Amazon SES

### Step 1: Set Up DynamoDB Table
```bash
aws dynamodb create-table \
    --table-name GroceryItems \
    --attribute-definitions \
        AttributeName=userEmail,AttributeType=S \
        AttributeName=itemName,AttributeType=S \
    --key-schema \
        AttributeName=userEmail,KeyType=HASH \
        AttributeName=itemName,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST
```

### Step 2: Configure Amazon SES
1. Verify your sender email address in SES console
2. Update the sender email in Lambda functions:
   - `saveGroceryItem.py` line 25
   - `sendExpiryReminders.py` line 25

### Step 3: Deploy Lambda Functions

#### Create IAM Role for Lambda
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:Scan",
                "dynamodb:PutItem",
                "ses:SendEmail",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

#### Deploy Functions
1. Create Lambda functions in AWS Console
2. Upload the respective Python/Node.js code
3. Set appropriate timeout (30 seconds recommended)
4. Configure environment variables if needed

### Step 4: Set Up API Gateway
1. Create REST API in API Gateway
2. Create resources and methods:
   - `POST /saveGroceryItem` → `saveGroceryItem` Lambda
   - `GET /grocery-items` → `getGroceryItems` Lambda
   - `OPTIONS /{proxy+}` → `handleCorsOptions` Lambda
3. Enable CORS for all endpoints
4. Deploy API and note the endpoint URLs

### Step 5: Update Frontend Configuration
Update the API URLs in `index.html`:
```javascript
const saveApiUrl = "YOUR_API_GATEWAY_URL/saveGroceryItem";
const getApiUrl = "YOUR_API_GATEWAY_URL/grocery-items";
```

### Step 6: Deploy Static Website
1. Create S3 bucket with static website hosting
2. Upload `index.html` to the bucket
3. Set bucket policy for public read access
4. Note the website endpoint URL

### Step 7: Set Up EventBridge Schedule
1. Create EventBridge rule with daily schedule
2. Set target as `sendExpiryReminders` Lambda function
3. Configure appropriate permissions

## 📖 Usage and Examples

### Adding a New Item
1. Open the web application
2. Fill in the form:
   - **Item Name**: "Milk"
   - **Expiry Date**: "2025-07-30"
   - **Email**: "user@example.com"
3. Click "Save Item"
4. Receive confirmation email immediately

### Viewing Saved Items
- Items appear automatically in the "Saved Grocery Items" section
- Statistics show total items and items expiring soon
- Items expiring within 3 days are highlighted in red

### Receiving Reminders
- System automatically checks daily for items expiring tomorrow
- Reminder emails sent at scheduled time
- Email includes item name and expiration date

### Example API Requests

#### Save Item
```bash
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/default/saveGroceryItem" \
     -H "Content-Type: application/json" \
     -d '{"itemName":"Bread","expiryDate":"2025-07-29","email":"user@example.com"}'
```

#### Get Items
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/default/grocery-items"
```

## 🔧 Troubleshooting and Support

### Common Issues

#### Email Not Sending
- **Check**: SES email verification status
- **Solution**: Verify sender email in SES console
- **Note**: Check spam folder for emails

#### CORS Errors
- **Check**: API Gateway CORS configuration
- **Solution**: Ensure all endpoints have CORS enabled
- **Verify**: OPTIONS method is properly configured

#### Items Not Saving
- **Check**: DynamoDB table permissions
- **Verify**: Lambda function has DynamoDB write permissions
- **Debug**: Check CloudWatch logs for errors

#### Frontend Not Loading Items
- **Check**: API Gateway endpoint URLs in JavaScript
- **Verify**: GET endpoint is accessible
- **Debug**: Check browser network tab for API responses

### Error Handling
- All Lambda functions include try-catch error handling
- Appropriate HTTP status codes returned
- Error messages logged to CloudWatch

### Support Resources
- AWS Documentation: [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- AWS Support: Available through AWS Console
- CloudWatch Logs: Monitor function execution and errors

## 📊 Monitoring and Maintenance

### CloudWatch Metrics
- Monitor Lambda function invocations
- Track error rates and duration
- Set up alarms for failures

### Cost Optimization
- DynamoDB on-demand pricing scales with usage
- Lambda charged per invocation and duration
- SES charges per email sent

### Regular Maintenance
- Review CloudWatch logs monthly
- Update email templates as needed
- Monitor DynamoDB item count growth

## 🤝 Contributing

We welcome contributions to improve the Smart Grocery Reminder App! Please follow these guidelines:

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow existing code style and conventions
- Add appropriate comments and documentation
- Test thoroughly before submitting
- Update README if adding new features

### Areas for Improvement
- Mobile app development
- Advanced notification preferences
- Integration with grocery store APIs
- Barcode scanning functionality
- Recipe suggestions based on expiring items

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- **Permissions**: Commercial use, modification, distribution, private use
- **Conditions**: License and copyright notice must be included
- **Limitations**: No liability or warranty provided

## 🙏 Acknowledgments

- AWS for providing excellent serverless services
- The open-source community for inspiration and best practices
- Contributors who help improve this project

## 📞 Contact

For questions, suggestions, or support:
- Create an issue in this repository
- Email: [your-email@example.com]
- AWS Community Forums: [AWS Developer Forums](https://forums.aws.amazon.com/)

---

**Built with ❤️ using AWS Serverless Technologies**# smart-grocery-remainder-app
