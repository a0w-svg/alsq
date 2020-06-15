module.exports = {
    name: 'user-info',
    description: 'Display info about yourself',
    execute(message) {

        message.channel.send(`Your Name: ${message.author.username}\nYour ID: ${message.author.id}`);
    },
};