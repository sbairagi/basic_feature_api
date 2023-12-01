from django.db import models

# Create your models here.

class Updateinfo(models.Model):
    allApps = (
    ('Stock Market Live', 'Stock Market Live'),
    ('Angel Learning Stock Market', 'Angel Learning Stock Market'),
    ('Live Share Tips Free', 'Live Share Tips Free'),
    ('Stock Of The Day - Intraday, BTST, Positional', 'Stock Of The Day - Intraday, BTST, Positional'),
    ('Everyday Intraday Tips Stock Banknifty Option', 'Everyday Intraday Tips Stock Banknifty Option'),
    ('Rise Investing - Stock, Niffty, Banknifty, Options', 'Rise Investing - Stock, Niffty, Banknifty, Options'),
    ('Upstocks Varsity', 'Upstocks Varsity'),
    ('Everyday Intraday Tips', 'Everyday Intraday Tips'),
    ('Share Market Course', 'Share Market Course'),
    ('Stock Axis - Free Stock Tips', 'Stock Axis - Free Stock Tips'),
    ('Free Intraday Tips Stocks MCX F & O', 'Free Intraday Tips Stocks MCX F & O'),
    ('Share Market Gurukul', 'Share Market Gurukul'),
    ('Stock Market Free Tips', 'Stock Market Free Tips'),
    ('Free Intraday Trading Tips', 'Free Intraday Trading Tips'),
    ('Share Market Tips', 'Share Market Tips'),
    ('Free Tranding Tips - Stock Market, Nifty 50', 'Free Tranding Tips - Stock Market, Nifty 50'),
    ('Free Tips - Equity, Stock, BankNifty, Option MCX', 'Free Tips - Equity, Stock, BankNifty, Option MCX'),
    ('Share Tips - Live Share Market Tips', 'Share Tips - Live Share Market Tips'),
    ('Stock Watch - Free Stock Tips', 'Stock Watch - Free Stock Tips'),
    ('Free Intraday Tips', 'Free Intraday Tips'),
    ('Stock Market Course', 'Stock Market Course'),
    ('Dhan Intraday Tips - Stock, Nifty, Banknifty, Options', 'Dhan Intraday Tips - Stock, Nifty, Banknifty, Options'),
    ('HugeProfit_Share_Market_Tips', 'HugeProfit_Share_Market_Tips'),
    ('Intraday Tips', 'Intraday Tips'),
    ('Stock Market Pulse', 'Stock Market Pulse'),
    ('Free Currency Tips Stock Market', 'Free Currency Tips Stock Market'),
    ('Angel Learning Stock Market', 'Angel Learning Stock Market'),
    ('Live Share Tips Daily Free Stock Tips MCX Advisory', 'Live Share Tips Daily Free Stock Tips MCX Advisory'),
    ('Angel Varsity Free Stock Market Course And Tips', 'Angel Varsity Free Stock Market Course And Tips')
)
    app_name = models.CharField(choices=allApps, unique=True, max_length=255, null=True, blank=True, help_text="If App Name is not found. You have to add App Name in models File")
    current_version = models.CharField(default='', null=True, blank=True, max_length=255, help_text="for ex. 0.1 , 0.8, 2.0, 2.2 ")
    maintenance_mode = models.CharField(default=False, null=True, blank=False, max_length=255, help_text="Switch False to remove app popup blocker alert for users to this app")
    Majortitle = models.CharField(default='', null=True, blank=True, max_length=255, help_text="App major update Title goes here")
    Majormsg = models.CharField(default='', null=True, blank=True, max_length=255, help_text="App major update Message goes here")
    Majorbtn = models.CharField(default='', null=True, blank=True, max_length=255, help_text="App major update Button Text goes here")
    Minortitle = models.CharField(default='', null=True, blank=True, max_length=255, help_text="App minor update Title goes here")
    Minormsg = models.CharField(default='', null=True, blank=True, max_length=255, help_text="App minor update Message goes here")
    Minorbtn = models.CharField(default='', null=True, blank=True, max_length=255, help_text="App minor update Button Text goes here")
    maintenance_title = models.CharField(default='', null=True, blank=True, max_length=255, help_text="maintenance Message goes here")
    maintenance_msg = models.CharField(default='', null=True, blank=True, max_length=255, help_text="maintenance Message goes here")


    def __str__(self):
        return self.app_name