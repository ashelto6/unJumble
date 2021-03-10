from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import db, TDSession
from .models import User
from dotenv import load_dotenv
from datetime import date
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
main = Blueprint('main', __name__)

#homepage route - GET
@main.route('/')
@main.route('/home')
def index():
	TDSession.login()
	#for large cap data 
	LCticklist=['DIS','TSLA','AMZN','MSFT'] #ticker list
	LCdata = TDSession.get_quotes(instruments=LCticklist)
	LCdata_list=[]
	for tick in LCticklist:
		LCdata_list.append(LCdata[tick])
	LCdata=LCdata_list

	#for mid cap data
	MCticklist=['RBLX','GME','RIOT'] #ticker list 
	MCdata = TDSession.get_quotes(instruments=MCticklist)
	MCdata_list=[]
	for tick in MCticklist:
		MCdata_list.append(MCdata[tick])
	MCdata=MCdata_list
	
	#for penny cap data
	PSticklist=['AMC','INPX','ZOM'] #ticker list 
	PSdata = TDSession.get_quotes(instruments=PSticklist)
	PSdata_list=[]
	for tick in PSticklist:
		PSdata_list.append(PSdata[tick])
	PSdata=PSdata_list
 
	today = date.today()
	today=today.strftime("%m/%d/%Y")
 
	return render_template("/main/index.html",  LCdata=LCdata, MCdata=MCdata, PSdata=PSdata, date=today)

#portfolio page route - GET
@main.route('/portfolio')
@login_required
def portfolio():
	TDSession.login()
	data = TDSession.get_accounts(account='all', fields=['positions'])
	today = date.today()
	today=today.strftime("%m/%d/%Y")
	return render_template('/main/portfolio.html', name=current_user.first_name, data=data, date=today)
 
#watchlist page route - GET
@main.route('/watchlist')
def watchlist():
	TDSession.login()
	data = TDSession.get_watchlist(account=os.environ.get('TD'), watchlist_id=os.environ.get('TDWL'))
	WLTickers = []
	for ticker in data['watchlistItems']:
		WLTickers.append(ticker['instrument']['symbol'])
	WLdata = TDSession.get_quotes(instruments=WLTickers)
 
	WLdata_list=[]
	for tick in WLTickers:
		WLdata_list.append(WLdata[tick])
	WLdata=WLdata_list
 
	today = date.today()
	today=today.strftime("%m/%d/%Y")
	return render_template('/main/watchlist.html', WLdata=WLdata, date=today)

#settings pages route - GET
@main.route('/settings')
@login_required
def settings():
 user=User.query.filter_by(email = current_user.email).first()
 today = date.today()
 today = today.strftime("%m/%d/%Y") 
 return render_template('/main/settings.html', current_user=user, date=today)

######################################### AJAX ROUTES ##############################################

#PSData AJAX route - POST
@main.route('/update_PSdata', methods=['POST'])
def updatePSdata():
	TDSession.login()
	PSticklist=['AMC','INPX','ZOM'] #ticker list
	PSdata = TDSession.get_quotes(instruments=PSticklist)
	PSdata_list=[]
	for tick in PSticklist:
		PSdata_list.append(PSdata[tick])
	PSdata=PSdata_list
	return jsonify('', render_template('/ajax/update_PSdata_model.html', PSdata=PSdata))

#MCdata AJAX route - POST
@main.route('/update_MCdata', methods=['POST'])
def updateMCdata():
	TDSession.login()
	MCticklist=['RBLX','GME','RIOT'] #ticker list
	MCdata = TDSession.get_quotes(instruments=MCticklist)
	MCdata_list=[]
	for tick in MCticklist:
		MCdata_list.append(MCdata[tick])
	MCdata=MCdata_list
	return jsonify('', render_template('/ajax/update_MCdata_model.html', MCdata=MCdata))

#LCdata AJAX route - POST
@main.route('/update_LCdata', methods=['POST'])
def updateLCdata():
	TDSession.login()
	LCticklist=['DIS','TSLA','AMZN','MSFT'] #ticker list
	LCdata = TDSession.get_quotes(instruments=LCticklist)
	LCdata_list=[]
	for tick in LCticklist:
		LCdata_list.append(LCdata[tick])
	LCdata=LCdata_list
	return jsonify('', render_template('/ajax/update_LCdata_model.html', LCdata=LCdata))

#######################################################################################