from odoo import models, fields, api

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_priority = fields.Many2one('x.player.priority', string='New Priority')
    x_player_position = fields.Many2one('x.player.position', string="Player's Position")
    x_player_nationality = fields.Many2one('x.player.nationality', string="Player's Nationality")
    x_country_request = fields.Many2one('res.country', string='Country request')
    x_file = fields.Binary(string='Upload your file')

    x_company_name = fields.Many2one(
        'res.company',
        string='Assigned Company',
        default=lambda self: self.env.company,
        index=True
    )

    x_contact_name = fields.Char(string="Contact name", compute="_compute_partner_info", store=True, readonly=True)
    x_mobile_from_contact = fields.Char(string="Mobile from Contact", compute="_compute_partner_info", store=True, readonly=True)

    other_contact = fields.Many2one('res.partner', string="Other Contact")

    x_secondary_stage = fields.Selection([
        ('first', 'First Status'),
        ('second', 'Second Status'),
        ('third', 'Third Status'),
    ], string="Secondary Status", default='first', tracking=True)

    @api.depends('partner_id')
    def _compute_partner_info(self):
        for rec in self:
            if rec.partner_id:
                rec.x_contact_name = rec.partner_id.name
                rec.x_mobile_from_contact = rec.partner_id.mobile
            else:
                rec.x_contact_name = False
                rec.x_mobile_from_contact = False

    def action_set_new_quotation(self):
        self.ensure_one()
        stage = self.env.ref('sportis_crm.crm_stage_new_quotation', raise_if_not_found=False)
        if stage:
            self.stage_id = stage.id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'x_company_name' not in vals:
                vals['x_company_name'] = self.env.company.id
            if not vals.get('name'):
                vals['name'] = self.env.context.get('default_name', 'New Lead')
        return super().create(vals_list)





class ResPartner(models.Model):
    _inherit = 'res.partner'

    decision_maker = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'Not'),
        ('unknown', "Don't know"),
    ], string="Decision maker")

    contact_qualification = fields.Many2one(
        'contact.qualification', string="Contact Qualification"
    )
    followup_by_id = fields.Many2one('res.users', string="Follow-up by")
    sport = fields.Many2one('res.company', string="Sport")

    # Novo polje koje se koristi u XML-u
    phone_secondary = fields.Char(string="Office phone")

    nature_of_company = fields.Char(string="Nature of company")
    level_of_playing = fields.Selection([
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('other', 'Other'),
    ], string="Level of playing")
    training_center = fields.Boolean(string="Training center")
    full_address = fields.Char(string="Address", compute="_compute_full_address")
    x_nature_of_company = fields.Many2one(
        'nature.of.company', string="Nature of Company"
    )
    country_location = fields.Many2one('res.country', string="Country Location")


    @api.depends('street', 'street2', 'zip', 'city', 'state_id', 'country_id')
    def _compute_full_address(self):
        for rec in self:
            address = ', '.join(filter(None, [
                rec.street,
                rec.street2,
                rec.zip,
                rec.city,
                rec.state_id.name if rec.state_id else '',
                rec.country_id.name if rec.country_id else ''
            ]))
            rec.full_address = address


class PlayerPriority(models.Model):
    _name = 'x.player.priority'
    _description = 'Player Priority'

    name = fields.Char(string="Priority", required=True)

class PlayerPosition(models.Model):
    _name = 'x.player.position'
    _description = 'Player Position'

    name = fields.Char(string="Position", required=True)

class PlayerNationality(models.Model):
    _name = 'x.player.nationality'
    _description = 'Player Nationality'

    name = fields.Char(string="Nationality", required=True)

class ContactQualification(models.Model):
    _name = 'contact.qualification'
    _description = 'Contact Qualification'

    name = fields.Char(string='Qualification', required=True)

class NatureOfCompany(models.Model):
    _name = 'nature.of.company'
    _description = 'Nature of Company'

    name = fields.Char(string="Nature", required=True)

class TodoTask(models.Model):
    _inherit = 'project.task'