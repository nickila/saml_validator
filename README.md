# flask_saml_validator -- {Name change needed}
https://adobe-saml-help.herokuapp.com/

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/michaelmernin/flask_saml_validator) -- could be added if this becomes available

The {name} is a saml response validator that will help assist with troubleshooting your sso integration with Adobe's admin console.  By uploading a saml trace of an attempted user login along with selecting your idp, you will be provided a user-friendly view of your .xml saml trace along with alerts of any common errors found and idp specific tips in order to solve any errors found.

# How to receive results

### Capture SAML Response and export trace as an .xml file
   > Please review the following link on necessary steps to capture the SAML response
   > https://helpx.adobe.com/enterprise/kb/perform-a-saml-trace.html
### Visit our application
https://adobe-saml-help.herokuapp.com/

### Browse and upload .xml file
  ![]() -- insert photo of application landing page
### Select your IDP from the drop-down box
  > If you do not see your IDP in the available options please select "Other" to continue with your results.
 ### Press SUBMIT
  > Your results will be shown (example in image below)
  
![]() -- insert photo of example results

# Understanding your results
The results will be a pretty print of the important values from your saml trace, including a description of the attribute's role in the saml response.    
If common errors are found the attribute will be bordered in red along with, if applicable, an explanation of the error's meaning and an idp-specific link to help you resolve the issue.
> please see "Result components further explained"(below) for an indepth description of a result's components


### Values being extracted and pretty printed in results
| Attribute | description | 
| ------ | ------ |
| name-id | name-id attribute being sent in SAML response |
| name-id format | Format of your Name-ID attribute |
| assertion attributes | Attributes included in your SAML assertion |
| destination (ACS) url | Must match Location attribute value from Adobe Metadata |
| issuer url (Entity ID) | Must match Entity ID attribute value from Adobe Metadata |
| In Response To | Id of SAML request, this response is created for |
| digest method algorithm | Should be rsa-sha1 |
| signature method algorithm | Should be rsa-sha1 |
| token signing certificate | must be Base-64 encoded X.509(.CER), which is equivalent to a PEM format certificate |
| time sent | Timestamp of response, must be within the 'not_before' and 'not_on_or_after' time window |
| not_before | Response must not before this timestamp value |
| not on or after | Response must not be on or after this timestamp value |

# Result components further explained
### Pretty Print
-- Insert a photo of an example result attribute, and highlight it's main components:
Name  
description  
value extracted 
### Errors Found
-- Insert a photo of an example error result and a description to explain it's components:  
description of error  
if applicable, link to idp-specific tips.
