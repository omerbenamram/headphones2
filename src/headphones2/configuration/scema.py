from marshmallow import Schema, fields, validates

from headphones2.utils.filesystem import is_pathname_valid


class ConfigurationSchema(Schema):
    libraryPath = fields.Str()
    debug = fields.Boolean()

    @validates('libraryPath')
    def validate_path(self, value):
        return is_pathname_valid(value)
