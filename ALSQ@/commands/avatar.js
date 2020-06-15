module.exports = {
    name: 'avatar',
    description: 'Get the avatar URL of the tagged user(s), or your own avatar.',
    execute(message) {
        if (!msg.mentions.users.size) {
            return msg.channel.send(`Your Avatar: <${message.author.displayAvatarURL({ format: "png", dynamic: true })}`);
        }

        const avatarList = message.mentions.users.map(user => {
            return `${user.username}'s avatar: <${user.displayAvatarURL({ format: "png", dynamic: true })}`;
        });

        message.channel.send(avatarList);
    },
};