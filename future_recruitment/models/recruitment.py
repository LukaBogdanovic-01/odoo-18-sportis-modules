from odoo import models, fields, api

class FutureRecruitment(models.Model):
    _name = 'future.recruitment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Future Recruitment'

    name = fields.Char(required=True)
    position_id = fields.Many2one('rec.position', string="Position")
    contact_id = fields.Many2one('res.partner', string="Contact")
    phone = fields.Char()
    email = fields.Char()
    country_id = fields.Many2one('res.country', string="Country")
    tag_ids = fields.Many2many('recruitment.tag', string="Tags")
    sport_id = fields.Many2one('res.company', string="Sport")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')
    ], default='0')
    file = fields.Binary(string="Attachment")
    create_date = fields.Datetime(readonly=True)
    agent_id = fields.Many2one('res.partner', string="Origin Agent invisible")
    origin_agent_id = fields.Many2one('origin.agent', string="Origin Agent")
    followup_by = fields.Many2one('res.users', string="Follow-up by")
    image = fields.Image()
    more_info = fields.Text(string="More Information")
    stage_id = fields.Many2one(
        'rec.kanban.stage',
        string="Stage",
        ondelete='set null',
        index=True,
        tracking=True,
        group_expand='_read_group_stage_ids',
    )

    career_ids = fields.Html( string="Career")
    award_ids = fields.Html( string="Awards")

    interview_date = fields.Datetime(string="Interview Date")

    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order=None):
        """Always show all stages in kanban"""
        return self.env['rec.kanban.stage'].search([], order=order)

    def export_records(self):
        """Export Future Recruitment zapisa u CSV"""
        import io
        import base64
        import csv

        # Ako korisnik nije selektovao ništa, exportuj sve
        records = self or self.search([])

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['Name', 'Position', 'Email', 'Phone', 'Country', 'Sport', 'Priority'])  # header
        for rec in records:
            writer.writerow([
                rec.name or '',
                rec.position_id.name or '',
                rec.email or '',
                rec.phone or '',
                rec.country_id.name or '',
                rec.sport_id.name or '',
                dict(self._fields['priority'].selection).get(rec.priority, ''),
            ])

        csv_data = buffer.getvalue()
        buffer.close()

        # Kreiraj attachment i ponudi download
        data = base64.b64encode(csv_data.encode('utf-8'))
        attachment = self.env['ir.attachment'].create({
            'name': 'future_recruitments_export.csv',
            'type': 'binary',
            'datas': data,
            'res_model': 'future.recruitment',
            'mimetype': 'text/csv',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }







class RecruitmentCareer(models.Model):
    _name = 'recruitment.career'
    _description = 'Career Record'

    name = fields.Char(string="Title")
    recruitment_id = fields.Many2one('future.recruitment', string="Candidate")
    date_start = fields.Date()
    date_end = fields.Date()
    description = fields.Text()



class RecruitmentAward(models.Model):
    _name = 'recruitment.award'
    _description = 'Award Record'

    name = fields.Char(string="Award Name", required=True)
    recruitment_id = fields.Many2one('future.recruitment', string="Candidate", required=True)
    date_awarded = fields.Date(string="Date Awarded")
    description = fields.Text(string="Details")


class RecruitmentTag(models.Model):
    _name = 'recruitment.tag'
    _description = 'Recruitment Tag'

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

class ResSport(models.Model):
    _name = 'res.sport'
    _description = 'Sport'

    name = fields.Char(required=True)

class RecPosition(models.Model):
    _name = 'rec.position'
    _description = 'Position'

    name = fields.Char(required=True)

class OriginAgent(models.Model):
    _name = 'origin.agent'
    _description = 'Origin Agent'

    name = fields.Char(required=True)


class KanbanStages(models.Model):
    _name = 'rec.kanban.stage'
    _description = 'Kanban stage'
    _order = 'sequence, id'

    name = fields.Char('Stage Name', required=True)                 
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean('Folded in Kanban')
    active = fields.Boolean(default=True)