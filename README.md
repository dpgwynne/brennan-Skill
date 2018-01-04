Welcome to the AWS CodeStar sample Alexa Skill
==============================================

This sample code helps get you started with a simple skill built with the
Amazon Alexa Skills Kit and deployed by AWS CloudFormation to AWS Lambda.

What's Here
-----------

This sample includes:

* README.md - this file
* buildspec.yml - This YAML file is used by AWS CodeBuild to create an artifact
  that can be used to deploy to AWS Lambda through CloudFormation.
* lambda_function.py - This file contains the AWS Lambda code used to interact with Alexa.
* template.yml - This YAML file is used by AWS CloudFormation to update AWS Lambda
  and manage any additional AWS resources.

Getting Started
---------------

To work on the sample code, you'll need to clone your project's repository to your
local computer. If you haven't, do that first. You can find instructions in the
AWS CodeStar user guide.

Before registering your custom Alexa skill in the
[Amazon Developer Portal](https://developer.amazon.com), you can manually test
your code in the AWS Lambda console.

1. Find the AWS Lambda created by CodeStar for your project by visiting the Project
   view within your CodeStar project. Click the link for the AWS Lambda resource.

2. Select your AWS Lambda from the list on the console.

3. Click Actions and then Test function.

4. From the Sample event template list, select one of the sample Alexa requests:

   * Alexa Start Session
   * Alexa Intent - MyColors
   * Alexa End Session

5. Choose Submit

6. After the test event is run, the Execution Results section will show the
   response returned by the AWS Lambda.

7. From this page, if you'd like to test other events, click Actions and Configure test event.


What Do I Do Next?
------------------

Once you've tested your AWS Lambda from the AWS Lambda console, you can start making
changes to your Alexa skill or register it on the Amazon Developer Portal.
We suggest heading over to Amazon Developer Portal and setting up your new
custom Alexa skill. You can follow the directions detailed at
http://amzn.to/1LzFrj6. Since your AWS Lambda is already set-up for you, you
can follow along starting at the "Sample Interaction Model for the Color
Expert Blueprint" section.

After you have your Alexa skill set-up, we suggest making a small change to
lambda_function.py so you can see how changes pushed to your repository are
automatically picked up by your project pipeline and deployed to AWS Lambda.
Once you've seen how that works, start developing your own code, and have fun!

Learn more about Serverless Application Model (SAM) and how it works here:
https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md

Learn more about AWS CodeStar by reading the user guide. Ask questions or make
suggestions on our forum.

User Guide: http://docs.aws.amazon.com/codestar/latest/userguide/welcome.html

Forum: https://forums.aws.amazon.com/forum.jspa?forumID=248