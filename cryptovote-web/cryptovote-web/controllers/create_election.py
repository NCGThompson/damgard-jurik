# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

blueprint = Blueprint('create_election', __name__)


@blueprint.route('/create')
def create_name():
    return render_template('create_election/election_name.html')


@blueprint.route('/verify-email')
def verify_email():
    return render_template('create_election/verify_email.html')


@blueprint.route('/verify-phone')
def verify_phone():
    return render_template('create_election/verify_phone.html')


@blueprint.route('/setup', subdomain='<election>')
def register_identity(election):
    return render_template('create_election/register_identity.html')


@blueprint.route('/register-authorities', subdomain='<election>')
def register_authorities(election):
    return render_template('create_election/register_authorities.html')


@blueprint.route('/register-voters', subdomain='<election>')
def register_voters(election):
    return render_template('create_election/register_voters.html')
