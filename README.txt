  # PC_AssistANT
  
  Developer - Yeshwanth Reddy, Gaurav Sharma
  
    How to run the PC Assistant -
      goto the location - "dist/PC_AssistANT/"
      and run the PC_AssistANT.
      It will start in background and you will be able to hear it.
      Make sure you sound is at audible level to hear it.


    Before You Use -
    Setting up few things in Linux -(Only for linux Users)
      You need to setup few things in linux for text to speech as it does not provide a built-in tts engine.
      This thing uses google_speech library which needs "sox" to make it work.

        sudo apt-get install sox
        sudo apt-get install lame
        sudo apt-get install libsox-fmt-mp3
        sudo apt-get insall scrot

        sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next
        sudo apt-get update
        sudo apt-get install ffmpeg

      The above packages are support for the google_speech to text engine. 
      without these, you won't be able to hear anything from your assistant.

    How to Stop PC_AssistANT -	(Windows users won't need this)  
      Once you open the PC assistant, you can close it by saying "Exit" or "Shutdown" voice commands.
      In case of Unhandled situations, you can just use the "STOP_PC_AssistANT" which is located in
        "PC_AssistANT/dist/PC_Assistant/Stop_PC_AssistANT/dist/Stop_PC_AssistANT/Stop_PC_AssistANT."
      You can also suspend it by saying "go to sleep" or "take some rest" commands also.

    Modes Available - 

      1. Learning Mode  - 
      Trigger words - learn, teach you
        example:  Start Learning
                  Activate Learning Mode
                  I want to teach you something

      How it works - 
        The learning process will have a MAIN TASK which you are going to teach.
          and the MAIN TASK is accompanied with several steps.
          each step can be taught by showing mouse and keyboardd movements or saying there is some typing included in it.
        example:   I want to teach it how to open an Application in my PC.
          1. I'll say that the MAIN TASK would be - (open an Application)
          2. Next the first step is to (press Windows + r key)
          3. when it starts tracking my mouse and keyboard, ill show it how to press Windows + r keys by doing it myself.
          4. then i say (completed). which will make it stop tracing your mouse and keyboard and ask you for the 2nd step.
          5. say the 2nd step is (dynamic typing)
          6. here it will ask us to narrate what we want to type.
          7. say (chrome).
          8. next say (stop typing) and it will ask if there is a next step, say (yes).
          9. in the 3rd step,(pressing Enter). show it how to press (Enter.)
          10. and once you show it how to press Enter, say (task completed.) This will end the learning session.

          11. Once teaching is done, you can just ask it to (open an Application) now.
          12. it will repeat all the steps shown by you.
          13. As the second step was dynamic typing, it will be asking you to narrate the application name.
          14. Just say (notepad) and (stop typing)
          15 It will open Notepad for You...!

    2. Dynamic Typing -
      Trigger words - (start typing)
        example:  start typing what i say
                  start dynamic typing

      The dynamic typing feature will type what ever you say.
      There are some keywords for some special actions.
      Like,
        Delete some words Say - (delete 1 word) or (delete 3 word)
        Delete a character Say - (delete 1 character) or (delete 5 characters)
        Delete the whole line Say - (delete the line) or (delete the whole line)
        Go to next line Say - (go to next line)
        gining a tab space Say - (tab space)

    3. Making do what you taught -
      If you taught it how to do something, then just use the sentence which you used in the MAIN TASK while teaching.
      Just like I said in the Teaching process - (open an application).
      It saves the learnt things in the name of MAIN TASK. i.e (open an Application) in our case.
      If you say MAIN TASK is to (open an Application), next time you want it to do it, Just say (open an Application).

    4. Sleep Mode - 
      Trigger word - go to sleep, take some rest
        example: go to sleep Assistant
      This will set your assistant in Sleep mode. It will be active in the Background but would not disturb your work in the foreground. The keywork "wake up" will set it to active mode again.
    
    5. Closing the PC assistant -
      Say - (exit) or (go to sleep)
      This mightbe your favourite command after your first use. ;}
