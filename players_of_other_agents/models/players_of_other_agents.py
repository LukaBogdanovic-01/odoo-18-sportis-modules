from odoo import models, fields

class PlayerOtherAgent(models.Model):
    _name = 'player.other.agent'
    _description = 'Player Other Agent'

    name = fields.Char(string="Name", required=True)
    sport = fields.Many2one('res.sport', string="Sport")
    position = fields.Many2one(
        'x.player.position',
        string="Position",
        related='lead_id.x_player_position',
        store=True,
        readonly=False
    )
    agent_id = fields.Many2one('res.users', string="Agent of origin")
    contact = fields.Char(string="Contact")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    country_id = fields.Many2one('res.country', string="Country")
    tag_ids = fields.Many2many('res.partner.category', string="Tags")
    priority = fields.Selection([
        ('0', 'None'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
    ], string="Priority")
    create_date = fields.Datetime(string="Created on", readonly=True)
    created_by = fields.Many2one('res.users', string="Created by", default=lambda self: self.env.user)
    notes = fields.Text(string="Notes")
    file = fields.Binary(string="Add File")
    image = fields.Binary(string="Image", attachment=True)
    state = fields.Selection([
        ('new', 'New other players'),
        ('checked', 'Level checked'),
        ('in_progress', 'In Progress - proposed'),
        ('done', 'Done'),
    ], default='new', string="Status")
    lead_id = fields.Many2one('crm.lead', string="CRM Lead")
    

