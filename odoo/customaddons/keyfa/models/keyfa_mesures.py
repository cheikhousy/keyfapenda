from odoo import api,models,fields


class keyfa_mesure(models.Model):
    _name = 'order.mesure'


    name = fields.Many2one('res.partner', string='Client')
    sale = fields.Many2one('sale.order', string='Bon de commande')
    mrp = fields.Many2one('mrp.production', string='Bon de production')


    date_mesure = fields.Date('Date mesure')
    #sexe = fields.Selection(selection=[('h', 'Homme'), ('f', 'Femme')] , string="Sexe")
    sexe = fields.Boolean('Homme')
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


    mesures = fields.One2many('order.mesure','name' , string='Mesures', limit=1)


class Sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    mesures = fields.One2many('order.mesure','sale' , string='Mesures', limit=1)

    def onchange_mesures_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment term
        - Invoice address
        - Delivery address
        """
        if  self.partner_id:
            for data in self.browse():
                    for mes in data.mesures:

                      self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return



class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    sale_mesures = fields.One2many('order.mesure' , 'mrp', compute='_compute_sale_mesures', string='Mesures client', help='Indicate the name of sales order.')


    @api.multi
    def _compute_sale_mesures(self):
     def get_parent_move1(move1):
        if move1.move_dest_id:
            return get_parent_move1(move1.move_dest_id)
        return move1

     for production1 in self:
         move1 = get_parent_move1(production1.move_finished_ids[0])
         production1.sale_mesures = move1.procurement_id and move1.procurement_id.sale_line_id and move1.procurement_id.sale_line_id.order_id.mesures or False
