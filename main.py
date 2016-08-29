import webapp2

sign_in = """
<html>
<head>
<title> Log- In </title>
</head>
<div style = "background-color: #53D2FC"
<body>
<h1><strong> Sign in</strong><h1>
<form action="/sign-in" method = "post">
<label> Name:
 	<input type = "text" name = "login" value ='%(login)s'>
    </label>
    %(login_error)s
    <br>
<label> Password:
    <input type = "password" name = "pword" value = ''>
    </label>
    %(pass_error)s

    <br>
<label> Verify Password:
    <input type = "password" name = "vpword" value = ''>


    </label>
    <br>

<label> Email(Optional):
    <input type = "text" name = "mail" value = '%(mail)s'>
</label>
 %(email_error)s
<br>
<div style = "color : red"> %(error)s </div>
 <input type="submit" value = "Submit"/>
 </form>
 </body>
 </div>
 </html>
 """


# create a function to write form with errors with empty placeholders for password and verify pass
class MainHandler(webapp2.RequestHandler):
    def write_form(self, login_error = "", email_error = "", pass_error = "", login = "", mail ="", error = ""):
        self.response.out.write(sign_in % { "login_error": login_error,
                                            "email_error": email_error,
                                            "pass_error": pass_error,
                                            "login": login,
                                            "mail": mail,
                                            "error": error,
                                                })


    def get(self):
        self.write_form()

    def post(self):
        name = self.request.get('login')
        password = self.request.get('pword')
        vpass = self.request.get('vpword')
        email = self.request.get('mail')
        s_name = name.split()
        zero = ' '
        nil = ''
        e_split = email.split()
        email_at = '@'
        email_dot = '.'
        email_check = email.find(email_at)
        email_check2 = email.find(email_dot)
        email_check3 = email.find(zero)

        #if nothing entered all fields flagged
        if (name == nil and password == nil and email == nil or name == nil and password == nil):
            self.write_form(nil, nil, nil, nil, nil, "Login information required.")
        #if username field is blank
        if (name == nil and password != nil and email == nil or name ==nil and password != nil and email != nil):
            self.write_form("Username required", nil, nil, nil, email, nil)
        #if space in user name
        if(len(s_name))  > 1 and name != nil:
            self.write_form("Username cannot have any spaces", nil, nil, name, email, nil )
        #if invalid password
        if(name != nil and password != nil and len(password) < 1 and password != vpass or name != nil and email != nil and password != nil and password != vpass and email_check > 0 and email_check2 > 0 and email_check3 < 0):
            self.write_form(nil, nil, "Invalid password", name, email, nil)

        #if password required
        if(name != nil and (len(s_name) < 1) and password == nil):
            self.write_form(nil,nil, "Password Required", name, email, nil)

        #if bad email given
        if(email != nil and email_check < 1 and email_check2 < 1):
            self.write_form(nil, "Invalid email", nil, name, email)

        #if successful security check. Login successful!
        if (len(s_name) == 1 and name != nil and len(password) >= 1 and password == vpass and email != nil and email_check > 0 and email_check2 > 0 and email_check3 < 0 or len(s_name) == 1 and name != nil and len(password) >= 1 and password == vpass and email == nil ):
            self.response.write("<strong>Welcome</strong> " + name + "!")
            oops = True

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign-in', MainHandler)
], debug=True)
