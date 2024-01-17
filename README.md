#  WhatsApp with MyAlice 
Introducing our latest innovation on the Odoo Marketplace: the WhatsApp Connector for Odoo! Seamlessly integrate your WhatsApp numbers from MyAlice directly into your Odoo environment, revolutionizing the way you communicate with your contacts. This powerful app simplifies and enhances your messaging experience, providing you with a range of features to streamline your communication processes.


# Prerequisites
- Python3.10
- Odoo 16
- WhatsApp with MyAlice 

### Setup WhatsApp with MyAlice 

- clone the repository from github. 
    ``` 
    git clone git@github.com:alice-labs/odoo-plugin.git
   ```
- Now copy the file path and past the path into the addons_path in odoo.conf file 
    ```
    addons_path = odoo16/addons,odoo-plugin
    ```

Now restart the server and login to odoo with ADMIN account.WhatsApp with MyAlice Will Visible in the app list. If don't Click on Apps and Update the app list as below screenshot.
![Whatsapp with MyAlice](https://i.ibb.co/SJmyBgF/1.png)

Click on Active button to Install Whatsapp With MyAlice app 


![Whatsapp with MyAlice](https://i.ibb.co/KLM5bkh/Screenshot-of-Odoo-Apps.jpg)


### Configuration
After Install the app we need to configure the app. 
- Permission to User
  - Goto: Settings > Users & Companies
  
![Whatsapp with MyAlice](https://i.ibb.co/hKntvgW/2.png)
  
  - Click on the user you want to give access to user. Add give MyAlice Whatsapp access to the user as below screenshot
  
![Whatsapp with MyAlice](https://i.ibb.co/LhYwVhG/3.png)

 Now click on save and Refresh the page. Now you will see Whatsapp With MyALice

![Whatsapp with MyAlice](https://i.ibb.co/ncNFFLF/4.png)


### Configuration With Secret Key
 Now we have to configure with MyAlice Whatsapp Secret Key. Click on Configuration and Click on  New.
![Whatsapp with MyAlice](https://i.ibb.co/7tL9zG9/5.png)

Now Give A Name, MyAlice Secret Key and Click Active and save it as Below. To connect with MyAlice click on Connect Button. 
After click on the Connect button if everything is correct you will see a message as below that API Connected Successfully

![Whatsapp with MyAlice](https://i.ibb.co/GCppWDC/7.png)


In this way the rest of all the lambda will create.

First Build the common Docker Image and then build the other docker images. 
To build image and run lambda locally follow the following commands

### Channels
Click on Channels from the menu and you will see all your channels as below.
![Whatsapp with MyAlice](https://i.ibb.co/hZGzKqw/8.png)

Click on your channels which Templates you want to get. You'll see a Get Template button. Click on that button to get all the Templates which are available for this channel. 
![](https://i.ibb.co/TbStY47/9.png)

### Templates

Click on Templates and you will see all your templates as below
![Whatsapp with MyAlice](https://i.ibb.co/WfQzxN3/10.png)

Now goto Contacts app. Goto To any contact. You will see a button Send Whatsapp Message
![Whatsapp with MyAlice](https://i.ibb.co/xjS31Xt/11.png)

Click on the button to send message. You have to select any tempate, a phone number with country code then you are good to send whatsapp message.If there is any variables available in the template then you can input variables values also

![Whatsapp with MyAlice](https://i.ibb.co/WDL1rBr/12.png)