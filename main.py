# import os
# import smtplib
# from email import encoders
# from email.mime.application import MIMEApplication
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.multipart import MIMEMultipart
# import time

# Programs suspicous extensions
programExtensions = ['exe', 'pif', 'application', 'gadget', 'msi', 'msp', 'com', 'scr', 'hta', 'cpl', 'msc', 'jar', 'reg']


# Script files extensions
scriptExtensions = ['bat', 'cmd', 'vb', 'vbs', 'js', 'jse', 'ws', 'wsf', 'wsc', 'wsh', 'ps1', 'ps1xml',
'ps2', 'ps2xml', 'psc1', 'psc2', 'msh', 'msh1', 'msh2', 'mshxml', 'msh1xml', 'msh2xml']

# Shortcuts extensions
shortcutsExtensions = ['scf', 'lnk', 'inf']

# Content that makes claims and promises
promisesContent = ['#1', '100% more', '100% free', '100% satisfied', 'additional income', 'be your own boss'
'best price', 'big bucks', 'billion', 'cash bonus', 'cents on the dollar', 'consolidate debt', 'double your cash',
'earn extra cash', 'earn money', 'eliminate bad credit', 'extra cash', 'extra income', 'expect to earn', 'fash cash',
'financial freedom', 'free access', 'free consulation', 'free gift', 'free hosting', 'free info', 'free investment',
'free membership', 'free money', 'free preview', 'free quote', 'free trial', 'full refund', 'get out of debt', 'get paid',
'giveaway', 'guaranteed', 'increase sales', 'increase traffic', 'incredible deal', 'lower rates', 'loswest price', 'make money',
'million dollars', 'miracle', 'money back', 'once in a lifetime', 'one time', 'pennies a day', 'potential earnings', 'prize',
'promise', 'pure profit', 'risk-free', 'satisfaction guaranteed', 'save big money', 'save up to', 'special promotion']

# Content that show urgency and pressure
pressureContent = ['act now', 'apply now', 'become a member', 'call now', 'click below', 'click here', 'get it now', 'do it today',
"don't delete", 'exclusive deal', 'get started now', 'important information regarding', 'information you requested', 'instant',
'limited time', 'new customers only', 'order now', 'please read', 'see for youself', 'sign up free', 'take action', "this won't last",
'urengt', 'what are you waiting for?', 'while supplies last', 'will not believe your eyes', 'winner', 'winning', 'you are a winner',
'you have been selected']

# Shady, spam and unethical content
shadyContent = ['bulk email', 'buy direct', 'cancel at any time', 'check or money order', 'congragulations', 'confidentiality', 'cures',
'dear friend', 'direct email', 'direct marketing', 'hidden charges', 'human growth hormone', 'internet marketing', 'lose weight',
'mass email', 'meet singles', 'multi-level marketing', 'no catch', 'no cost', 'no credit check', 'no fees', 'no gimmick',
'no hidden costs', 'no hidden fees', 'no interest', 'no investment', 'no obligation', 'no purchase necessary', 'no questions asked',
'no strings attached', 'not junk', 'notspam', 'obligation', 'passwords', 'requires initial investment', 'social security number', "this isn't a scam",
"this isn't junk", "this isn't spam", 'undisclosed', 'unsecured credit', 'unsecured debt', 'unsolicited', 'valium', 'viagra', 'vicodin',
'we hate spam', 'weight loss', 'xanax']

# Spam related to legalese content
legaleseContent = ['accept credit cards', 'ad', 'all new', 'as seen on', 'bargain', 'beneficiary', 'billing', 'bonus', 'cards accepted', 'cash',
'certified', 'cheap', 'claims', 'clearance', 'compare rates', 'credit card offers', 'deal', 'debt', 'discount', 'fantastic', 'in accordance with laws',
'income', 'investment', 'lifetime', 'loans', 'luxury', 'marketing solution', 'message contains', 'mortgate rates', 'name brand', 'offer',
'online marketing', 'opt in', 'pre-approved', 'quote', 'rates', 'refinance', 'removal', 'reserves the right', 'score', 'search engine', 'sent in compliance',
'subject to', 'terms and conditions', 'trial', 'unlimited', 'warranty', 'web traffic', 'work from home']

wordsToLook = programExtensions + scriptExtensions + shortcutsExtensions + promisesContent + pressureContent + shadyContent + legaleseContent



def detect_suspicous_content(header_list):
    for word in wordsToLook:
        if word in header_list:
            return 1
    return 0
