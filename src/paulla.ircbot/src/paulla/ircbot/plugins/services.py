from configparser import ConfigParser
import irc3

config = ConfigParser()
config.read('services.cfg')
items = config.items('config')
thedict = {key: value.splitlines()[1:] for key, value in items}

@irc3.plugin
class ServicesPaulla:
    """ Services Paulla plugin """
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log
    
    @irc3.event(irc3.rfc.PRIVMSG)
    def services_paulla(self, mask, event, target, data):
        if '!service' in data:
            if [values for values in thedict.values() for values in values if '%s' % values in data]:
                if mask.nick != self.bot.nick:
                    valuestokeep = [values for values in thedict.values() for values in values if '%s' % values in data]
                    listkeys = [keys for keys, values in thedict.items() for values in values if values in valuestokeep]
                    if listkeys:
                        for thekey in listkeys:
                            self.bot.privmsg(target, "%s, il y a ce service au besoin : https://%s.paulla.asso.fr/" % (mask.nick, thekey))
            else:
                listkeys = [keys for keys, values in thedict.items()]
                self.bot.privmsg(target, "Tu en veux du service? Voilà ce qu'on a à ta dispo => %s.Alors tapes !service ainsi que le service dans cette liste et tu auras l'url voulue." % (', '.join(listkeys)))
                
