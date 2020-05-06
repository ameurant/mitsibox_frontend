# -*- coding: utf-8 -*-

import json
#import mysqlx
from plone import api
from Products.Five import BrowserView
from zope.interface import implements
from interfaces import IManageDisplayBox
from connexion_db import ConnexionDb

class DisplayBox(ConnexionDb):
    """
    recupère toutes les news et les renvoie en JSON
    """
    implements(IManageDisplayBox)
    
    def getJsonBox(self):
        """
        récupère les paramètres des boites au format JSON
        """
        session = self.getConnexion()
        db=session.get_schema('sensihold_v2')
        tables = db.get_tables()
        
        tbl_sensihold_mitisibox = db.get_collection('mitisibox_boxes')
        recs = tbl_sensihold_mitisibox.find().execute()
        myBoxes = recs.fetch_all()
        
        idList=[]
        for el in recs.fetch_all():
            idList.append(dict(el))
        boites = json.dumps(idList)
        return boites


    def getListingBox(self):
        """
        Récupères les infos des boites
        """
        session = self.getConnexion()

        db=session.get_schema('sensihold_v2')
        tables = db.get_tables()
        
        tbl_sensihold_mitisibox = db.get_collection('mitisibox_boxes')
        recs = tbl_sensihold_mitisibox.find().execute()
        #recs = tbl_sensihold_mitisibox.select().execute()
        myBoxes = recs.fetch_all()
        
        return myBoxes

    def getOneBox(self, idBox):
        """
        Récupères les infos des boites
        """

        session = self.getConnexion()

        db=session.get_schema('sensihold_v2')
        tables = db.get_tables()
        
        tbl_sensihold_mitisibox = db.get_collection('mitisibox_boxes')
        recs = tbl_sensihold_mitisibox.find("_id=='%s'"%(idBox,)).execute()
        myBoxe = recs.fetch_one()
        
        return myBoxe

        #box=col.find("_id=idBox").execute()