from odoo import api,models,fields


class keyfa_mesure(models.Model):
    _name = 'order.mesure'


    name = fields.Many2one('res.partner', string='Client')
    sale = fields.Many2one('sale.order', string='Bon de commande')
    sale_line = fields.Many2one('sale.order.line', string='Ligne Bon de commande')
    mrp = fields.Many2one('mrp.production', string='Bon de production')


    date_mesure = fields.Date('Date mesure')
    sexe = fields.Selection(selection=[('h', 'Homme'), ('f', 'Femme')] , string="Mesure pour : ")
    Long_Ep = fields.Integer("Longueur Epaule")
    Tour_Cou = fields.Integer("Tour de cou")
    C_Bat = fields.Integer("C_bat")
    V_Pince = fields.Integer("Valeur pince")
    H_Poitr = fields.Integer("Hauteur poitrine")
    T_Poitr = fields.Integer("Taille poitrine")
    Ceint = fields.Integer("Ceinture")
    T_Bass = fields.Integer("Taille bassin")
    L_Manc = fields.Integer("Longueur Manche")
    L_Manch3_4 = fields.Integer("Longueur Manche 3/4")
    T_Bras = fields.Integer("Tour bras")
    T_Poig = fields.Integer("Tour poignet")
    T_Cuiss = fields.Integer("Taille Cuisse")
    L_Genou = fields.Integer("Longuer Genoux")
    T_Veste = fields.Integer("taille Veste")
    T_Chem = fields.Integer("taille Chemise")
    T_Pant = fields.Integer("taille Pantalon")
    T_Stat = fields.Integer("taille Stature")
    #Style = fields.selection(('slim','SLIM'),('normal','NORMAL'),('large','LARGE'))
    Gabarit = fields.Boolean('Gabarit')
    Broderie   = fields.Selection((('ton_sur_ton','TON SUR TON'),('leg_ton_ton','LEGEREMENT TON SUR TON'),
                              ('flashy','FLASHY')))






class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'


    mesures = fields.One2many('order.mesure', 'name', string='Mesures')




class Sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    mesures = fields.One2many('order.mesure','sale' , string='Mesures')




class Sale_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'

    mesures = fields.One2many('order.mesure','sale_line' , string='Mesures')

    @api.onchange('mesures')
    def onchange_mesures(self):
        """
        Charger les mesures dans le bon de commande quand le client est choisi:

        """
        values = {
            'mesures': self.order_partner_id.mesures and self.order_partner_id.mesures or False,
        }
        self.update(values)




class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    sale_mesures = fields.One2many('order.mesure' , 'mrp', compute='_compute_sale_mesures', string='Mesures client', help='Indicate the name of sales order.')


    @api.multi
    def _compute_sale_mesures(self):
     def get_parent_move(move):
        if move.move_dest_id:
            return get_parent_move(move.move_dest_id)
        return move

     for production in self:
         move = get_parent_move(production.move_finished_ids[0])
         production.sale_mesures = move.procurement_id and move.procurement_id.sale_line_id and move.procurement_id.sale_line_id.mesures or False
