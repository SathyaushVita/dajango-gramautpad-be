class RegisterRouter:
    """
    A router to control all database operations on models in the
    Login model.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read Login models go to gramadevata_updated1.
        """
        if model.__name__ in ['User', 'Block', 'District', 'State', 'Country', 'Village']:
            return 'gramadevata_updated1'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write Login models go to gramadevata_updated1.
        """
        if model.__name__ in ['User', 'Block', 'District', 'State', 'Country', 'Village']:
            return 'gramadevata_updated1'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the Login model is involved.
        """
        if obj1.__class__.__name__ in ['User', 'Block', 'District', 'State', 'Country', 'Village'] or \
           obj2.__class__.__name__ in ['User', 'Block', 'District', 'State', 'Country', 'Village']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the models only appear in the 'gramadevata_updated1' database.
        """
        if model_name in ['User', 'Block', 'District', 'State', 'Country', 'Village']:
            return db == 'gramadevata_updated1'
        return db == 'default'
