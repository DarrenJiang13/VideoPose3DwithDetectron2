# Installation tutorial for AWS (Amazon Web Services) 

This is a tutorial to install a ec2 instance (`AWS Deep Learning Base AMI (Ubuntu 18.04)`)  
refer 1: https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/EC2_GetStarted.html  
refer 2: https://www.guru99.com/creating-amazon-ec2-instance.html  
refer 3: 

## 1. Starting a ec2 instance
[reference](https://www.guru99.com/creating-amazon-ec2-instance.html) with pictures
  1. Open the official site of [aws](https://aws.amazon.com/), then click the **"Sign in to the console"** button in the right top, register your account and sign in.
  2. Open your [AWS Management Console](https://console.aws.amazon.com/ec2/).From the console dashboard, choose **Launch instance**.
  3. Now you are able to follow the page step by step:
  - **Step 1: Choose an Amazon Machine Image (AMI)**. Search for "DLAMI 18.04 base", and select `AWS Deep Learning Base AMI (Ubuntu 18.04)` in **AWS Marketplace**,continue;
  - **Step 2: Choose an Instance Type**. Choose **t2.small** at the beginning, you will need to resize it if your code needs more computation power.
  
    (**GPU reminder**: If you want a GPU enabled instance, please choose the right type. You may need to apply for a GPU instance. for me, I use p2.xlarge)
  - **Step 3: Configure Instance Details**. You may set everything in this page as default. [pictures](https://www.guru99.com/creating-amazon-ec2-instance.html#4)
  - **Step 4: Add Storage**. Resize the **Size (GiB)** to 50, uncheck "Delete on Termination".
  - **Step 5: Add Tags**. Add Tags if you want.
  - **Step 6: Configure Security Group**. Must set **Type**:SSH, **Protocol**:TCP **Port Range**:22 to enable connection between your computer and this instance. It is ok to set source as 0.0.0.0/0 in this project
  - **Step 7: Review Instance Launch**. Review your configuration and launch your instance.
  - **Step 8: KeyPair**. If you create the instance for the first time, you will be asked to create a keypair yourself. You can name it as "NameKeyPair", e.g."DarrenKeyPair". Download the `NameKeyPair.pem` file for future use.
  4. Check instance states: you can check the states of your instance in [Instance Console](https://console.aws.amazon.com/ec2/)
,click the bold **Instances** to unfold the menu and then choose **Instances**.
  5. Select your own instance and you will see in the **Instance State** column, there is a green light and "running" sign. Wait for the instance to finish initialization.
  If the **Instance State** does not change for a while(more than 5 minutes), click **Status Checks** to update the state.
  6. click **Actions** button, choose "Instance State --> Stop" to stop the instance when you want to stop.
  
## 2. Connect to your instance
  1. Choose your own instance in [Instance Console](https://console.aws.amazon.com/ec2/), then click the **Connect** button in the top.You will see three options to connect to your instance. 
  2. Here I use "ssh". `cd` to the directory where you save your `KeyPair.pem` file, and type the command in the **Connect** page, which looks like:
    
    chmod 400 NameKeyPair.pem
    ssh -i "NameKeyPair.pem" ubuntu@ec2-3-15-152-189.us-east-2.compute.amazonaws.com
    
  3. Are you sure you want to continue connecting (yes/no)? choose **yes**. Now we are in!
