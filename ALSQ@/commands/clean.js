module.exports = {
    name: 'clean',
    description: 'delete up 99 messages',
    execute(message, args) {

        const value = parseInt(args[0]) + 1;

        if (isNaN(value)) {

            return message.reply('that doesn\'t seem to be a valid number.');
        }
        else if (value <= 1 || value > 100) {

            return message.reply('you need to input a number between 1  and 99');
        }

        message.channel.bulkDelete(value, true).catch(err => {

            console.error(err);
            message.channel.send('there was an error  trying delete messages in this channel! :(');
        });
    }
};