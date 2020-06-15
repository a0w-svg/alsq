module.exports = {
    name: 'kick',
    description: 'kick  user',
    execute(message) {
        if (!message.mentions.users.size) {
            return message.reply('you need to tag user in order to kick them!');
        }
        const taggedUser = message.mentions.users.first();
        message.channel.send(`You wanted to kick: ${taggedUser.username}`);
    }
};