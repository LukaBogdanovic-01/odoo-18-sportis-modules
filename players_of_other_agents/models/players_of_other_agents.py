from odoo import models, fields, api

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
    tag_ids = fields.Many2many('pota.tag', string="Tags")#('res.partner.category', string="Tags")
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
    stage_id = fields.Many2one(
        'pota.kanban.stage',
        string='Stage',
        ondelete='set null',
        index=True,
        tracking=True,
        group_expand='_read_group_stage_ids',
    )

    state = fields.Selection([ ('new', 'New other players'), ('checked', 'Level checked'), ('in_progress', 'In Progress - proposed'), ('done', 'Done'), ], default='new', string="Status", tracking=True, group_expand='_read_group_state')
    lead_id = fields.Many2one('crm.lead', string="CRM Lead")
    career_ids = fields.Html( string="Career")

    contract_date = fields.Datetime(string="Contract Date")


    @api.model
    def _read_group_stage_ids(self, stages, domain, order=None, **kwargs):
        """Always show all stages in kanban and statusbar"""
        return self.env['pota.kanban.stage'].search([], order=order or 'sequence, id')

    def export_records(self):
        """Export selektovanih agenata u CSV fajl"""
        import io
        import base64
        import csv

        # ako korisnik nije selektovao ništa, exportuj sve
        records = self or self.search([])

        # napravi CSV u memoriji
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['Name', 'Sport', 'Email', 'Phone', 'Country'])  # zaglavlje
        for rec in records:
            writer.writerow([
                rec.name or '',
                rec.sport.name or '',
                rec.email or '',
                rec.phone or '',
                rec.country_id.name or ''
            ])
        csv_data = buffer.getvalue()
        buffer.close()

        # napravi attachment
        data = base64.b64encode(csv_data.encode('utf-8'))
        attachment = self.env['ir.attachment'].create({
            'name': 'other_agents_export.csv',
            'type': 'binary',
            'datas': data,
            'res_model': 'player.other.agent',
            'mimetype': 'text/csv',
        })

        # otvori ga u browseru
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }



    
class PotaTag(models.Model):
    _name = 'pota.tag'
    _description = 'Pota Tag'

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")

    @api.model_create_multi
    def create(self, vals_list):
        count = self.search_count([])   # koliko već tagova postoji
        for vals in vals_list:
            if not vals.get("color"):
                vals["color"] = count % 12
                count += 1  # uvećaj brojač da svaki novi dobije narednu boju
        return super().create(vals_list)

class PotaOriginAgent(models.Model):
    _name = 'pota.origin.agent'
    _description = 'Origin Agent'

    name = fields.Char(required=True)

class RecPosition(models.Model):
    _name = 'pota.position'
    _description = 'Position'

    name = fields.Char(required=True)

class KanbanStages(models.Model):
    _name = 'pota.kanban.stage'
    _description = 'Kanban stage'
    _order = 'sequence, id'

    name = fields.Char('Stage Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean('Folded in Kanban')  
    active = fields.Boolean(default=True)                     
