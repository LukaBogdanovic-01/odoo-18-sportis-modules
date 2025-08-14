from odoo import models, fields

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
    image = fields.Image()
    more_info = fields.Text(string="More Information")
    state = fields.Selection([
        ('new', 'Nouveau - à recruter'),
        ('in_progress', 'En cours'),
        ('done', 'Fait')
    ], string='Status', default='new', tracking=True)

    stage_id = fields.Many2one('rec.kanban.stages', string='Stage')

    career_ids = fields.One2many('recruitment.career', 'recruitment_id', string="Career")
    award_ids = fields.One2many('recruitment.award', 'recruitment_id', string="Awards")



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
    _name = 'rec.kanban.stages'
    _description = 'Kanban stages'
    _order = 'sequence, id'

    name = fields.Char('Stage Name', required=True)
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean('Folded in Kanban')