.. _developer_guide:

Developer Guide
========================================================================

Source Code
------------------------------------------------------------------------

The source code can be found on github in the `err-backend-discord repository <https://github.com/errbotio/err-backend-discord>`_

Person Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Discord identity system doesn't map directly to that of errbots.  The below table attempts to align them as best possible for practical use.


   .. csv-table:: Class attributes
        :header: "Discord ``ClientUser``", "Description", "Errbot ``Person``", "Description"
        :widths: 10, 20, 10, 20

        ``name :str:``, "The user's username.", ``person :str:``, "a backend specific unique identifier representing the person you are talking to."
        ``id :int:``, "The user's unique ID.", ``client :str:``, "a backend specific unique identifier representing the device or client the person is using to talk."
        ``discriminator :str:``, "The user's discriminator. This is given when the username has conflicts."
        ``bot :bool:``, "Specifies if the user is a bot account.",         ``nick :str:``, "a backend specific nick returning the nickname of this person if available."
        ``system :bool:``, "Specifies if the user is a system user (i.e. represents Discord officially).", ``aclattr :str:``, "returns the unique identifier that will be used for ACL matches."
        ``??``, "??", ``fullname :str:``, "the fullname of this user if available."
        ``??``, "??", ``email :str:``, "the email of this user if available."


Room Occupant Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. csv-table:: Class attributes
        :header: "Discord ``??``", "Description", "Errbot ``RoomOccupant``", "Description"
        :widths: 10, 20, 10, 20

        ``??``, "??", ``room :any:``, "the fullname of this user if available."


Room Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. csv-table:: Class attributes
        :header: "Discord ``??``", "Description", "Errbot ``Room``", "Description"
        :widths: 10, 20, 10, 20

        ``??``, "??", ``join()``, "If the room does not exist yet, this will automatically call `create` on it first."
        ``??``, "??", ``leave()``, "Leave the room."
        ``??``, "??", ``create()``, "Create the room or do nothing if it already exists."
        ``??``, "??", ``destroy()``, "Destroy the room or do nothing if it doesn't exists."
        ``??``, "??", ``aclattr :str:``, "returns the unique identifier that will be used for ACL matches."
        ``??``, "??", ``exists :bool:``, "Returns ``True`` if the room exists, `False` otherwise."
        ``??``, "??", ``joined :bool:``, "Returns ``True`` if the room has been joined, `False` otherwise."
        ``??``, "??", ``topic :bool:``, "Returns the topic (a string) if one is set, ``None`` if notopic has been set at all."
        ``??``, "??", ``occupants :list:``, "Returns a list of occupant identities."
        ``??``, "??", ``invite()``, "Invite one or more people into the room."


Identification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Full identification requires to following fields:
::

        "guild_id": "012345678901234567"
        "channel_id": "123456789012345678",
        "author": {
            "username": "bumblebee",
            "public_flags": 0,
            "id": "234567890123456789",
            "discriminator": "0413",
            "bot": true,
            "avatar_decoration": null,
            "avatar": "5dba11479834e662c5e6a71807a3b9c3"
        },

The following examples show how errbot receives message events for identifier resolution

user mention text
::

    frm = username#1234@playground
    username = username#1234@playground
    text = .whoami <@123456789012345678>

channel mention text
::

    frm = username#1234@playground
    username = username#1234@playground
    text = .whoami <#123456789012345678>

raw text
::

    frm = username#1234@channel_name
    username = username#1234@channel_name
    text = .whoami username#1234@channel_name

guild mentions don't exists but could be represented with a string like ``<$123456789012345678>`` which would produce the following text identification representation to be resolved.
::

    #channel_name$guild_vanity_url_code
    #channel_name
    @username#1234



Contributing
------------------------------------------------------------------------

The process for contributing to the discord backend follows the usual github process as described below:

1. Fork the github project to your github account.
2. Clone the forked repository to your development machine.
3. Create a branch for changes in your locally cloned repository.
4. Develop feature/fix/change in your branch.
5. Push work from your branch to your forked repository
6. Open pull request from your forked repository to the official err-backend-discord repository.
