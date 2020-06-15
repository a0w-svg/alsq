const fs = require('fs');
const Discord = require('discord.js');
const { prefix, token } = require('./config.json');

const client = new Discord.Client();
client.commands = new Discord.Collection();


const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {

    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
}

const cooldowns = new Discord.Collection();

client.on('ready', () => {

    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {

    if (!msg.content.startsWith(prefix) || msg.author.bot) {
        return;
    }

    const args = msg.content.slice(prefix.length).split(/ +/);
    const commandName = args.shift().toLowerCase();
    

    const command = client.commands.get(commandName) || client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));

    if (!command) return;

    if (command.args && !args.length) {

        let reply = `You didn't provide any arguments, ${msg.author}`;

        if (command.usage) {

            reply += `\nThe proper usage would be: \`${prefix}${command.name} ${command.usage}\``;
        }

        return msg.channel.send(reply);
    }

    if (command.guildOnly && message.channel.type !== 'text') {

        return msg.reply('I can\'t  execute that command inside DMs');
    }

    if (!cooldowns.has(command.name)) {

        cooldowns.set(command.name, new Discord.Collection());
    }

    const now = Date.now();
    const timestamps = cooldowns.get(command.name);
    const cooldownAmount = (command.cooldowns || 3) * 1000;

    if (timestamps.has(msg.author.id)) {

        const expirationTime = timestamps.get(msg.author.id) + cooldownAmount;

        if (now < expirationTime) {
          
            const time_left = (expirationTime - now) / 1000;
            return msg.reply(`Please wait ${time_left.toFixed(1)} more second(s) before reusing the \`${command.name}\` command`);
        }
    }

    timestamps.set(msg.author.id, now);
    setTimeout(() => timestamps.delete(msg.author.id), cooldownAmount);

    try {

        command.execute(msg, args);
    }
    catch (error) {

        console.error(error);
        msg.reply('there was an error trying to execute that command!');
    }
    console.log(msg.content);
});

client.login(token);