from odoo import models, fields

class PlayerOtherAgent(models.Model):
    _name = 'player.other.agent'
    _description = 'Player Other Agent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    sport = fields.Many2one('res.company', string="Sport")
    position = fields.Many2one(
        'pota.position',
        string="Position",
        related='lead_id.x_player_position',
        store=True,
        readonly=False
    )
    agent_id = fields.Many2one('res.users', string="Agent of origin")
    origin_agent_id = fields.Many2one('pota.origin.agent', string="Origin Agent")
    followup_by = fields.Many2one('res.users', string="Follow-up by")
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
    created_by = fields.Many2one('res.users', string="Created  by", default=lambda self: self.env.user)
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
    career_ids = fields.Html( string="Career")

    stage_id = fields.Many2one('pota.kanban.stages', string='Stage')
    


class PotaOriginAgent(models.Model):
    _name = 'pota.origin.agent'
    _description = 'Origin Agent'

    name = fields.Char(required=True)

class RecPosition(models.Model):
    _name = 'pota.position'
    _description = 'Position'

    name = fields.Char(required=True)

class KanbanStages(models.Model):
    _name = 'pota.kanban.stages'
    _description = 'Kanban stages'
    _order = 'sequence, id'

    name = fields.Char('Stage Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean('Folded in Kanban')