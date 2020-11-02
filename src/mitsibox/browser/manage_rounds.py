# -*- coding: utf-8 -*-

import json
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from interfaces import IManageRounds
from connexion_db import ConnexionDb


class ManageRounds(ConnexionDb):
    """
    gestion des tournées
    """
    implements(IManageRounds)

    def getAllRounds(self):
        """
        Récupère les infos de toutes les tournées
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')

        tbl_mitsiround = db.get_collection('mitsibox_rounds')
        recs = tbl_mitsiround.find().execute()
        myRounds = recs.fetch_all()
        return myRounds

    def getRoundById(self, idRound):
        """
        Récupère les infos d'une tournée selon son _id
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')

        tbl_mitsiround = db.get_collection('mitsibox_rounds')
        recs = tbl_mitsiround.find("_id=='%s'"%(idRound,)).execute()
        myRound = recs.fetch_one()
        return myRound

    def getRoundsOfBox(self, idBox):
        """
        Récupère le nom dde la tournée à la quelle appartient une box
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')

        #select doc->>"$.roundName" from mitsibox_rounds where '00005f0d88fe0000000000000003' member of (doc->>'$.roundMitsiboxList');
        myRound = db.session.sql("""select
                                        doc->>"$.roundName"
                                    from
                                        mitsi_chuhautesenne.mitsibox_rounds
                                    where
                                        "%s" member of (doc->>'$.roundMitsiboxList')""" % (idBox,)).execute()

        return myRound.fetch_one()[0]

    def insertRound(self):
        """
        insertion d'une nouvelle tournée
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        round = db.get_collection('mitsibox_rounds')

        fields = self.request.form

        newRound = {}
        newRound['roundName'] = fields.get('roundName', None).decode("utf-8")
        newRound['roundType'] = fields.get('roundType', None)
        newRound['roundStartTime'] = fields.get('roundStartTime', None)
        newRound['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        newRound['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)

        round.add(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La tounrée est enregistrée."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-tournees/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''

    def updateRound(self):
        """
        modification d'une tournée
        """
        session = self.getConnexion()
        db = session.get_schema('mitsi_chuhautesenne')
        round = db.get_collection('mitsibox_rounds')

        fields = self.request.form
        idRound = fields.get('idRound', None) 

        newRound = {}
        newRound['roundName'] = fields.get('roundName', None).decode("utf-8")
        newRound['roundType'] = fields.get('roundType', None)
        newRound['roundStartTime'] = fields.get('roundStartTime', None)
        newRound['roundEstimedTime'] = fields.get('roundEstimedTime', None)
        newRound['roundMitsiboxList'] = fields.get('roundMitsiboxList', None)

        round.modify("_id='%s'" % idRound).patch(newRound).execute()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Les données de la tounrée ont été modifiées."
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/gestion-des-tournees/listing-des-tournees" % (portalUrl,)
        self.request.response.redirect(url)
        return ''
