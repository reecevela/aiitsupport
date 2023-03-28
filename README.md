# aiitsupport
GPT-Based IT Support that utilizes context and previous examples, mostly just learning how to use GPT-3.5-turbo and feed it information to help it be a better problem solver for businesses.

Available on [https://www.aiitsupport.net](https://www.aiitsupport.net) - it's still under development so report any issues here or in the contact section on the homepage - I'll get your email.
 
 I've removed a lot of the core functionality and personal info, but overall what it does is:
 
   - Keep a Postgres database with three tables - Users, Supported Apps, and Troubleshooting Examples
   - Has a Many-toMany relationship between users and supported apps, so examples for one company's Outlook will be loaded into another company's outlook troubleshooting as well so it can learn as quickly as possible.
   - Whenever a user mentions a name of a supported app in their input, it loads all of the troubleshooting examples for that app into the conversation so that Ruby can have a better idea of how to solve problems
   - It also front-loads a lot of information for faster troubleshooting based off of user settings, like computer OS so that it doesn't have to suggest how to add a printer on both Mac and Windows, for example.
   - With the ability for users to add their own troubleshooting examples, it can support applications that are more recent than OpenAI's model's info (~2021) and can also support custom in-house applications.
   
In the future, I'm planning on adding automatic entry into the troubleshooting examples when a user clicks that a problem has been resolved, so that it learns by itself. It will also need automatic database cleanup functionality, but for now this is just in the MVP stage and I'll be adding many more features on the official site.

Also I'll note that this is my first django project, first GPT-based project, and first fullstack project! I'm glad to see it coming together, I've been on the front-end for a while but it's really awesome to have this much freedom with my app!

A few of the things I learned while making this:
 - Vim
 - Django
 - Postgres and how databases work
 - SSH much more in-depth
 - Gunicorn
 - Nginx
 - Setting up SSL
