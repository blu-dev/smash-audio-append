# smash-audio-append
Adds entries to both the NUS3Bank files and soundlabelinfo.sli file
Python 3+ is required

## Usage
Make sure you use nus3append first, since it will give you the entry number you need to use for sli_patch.

sli_patch is only used for adding sound effects, I'm pretty sure.

Example (announcer calls):
```
python nus3append.py
Enter the path of your file: vc_narration_characall.nus3bank
Enter the name of the appended sound effect: vc_narration_characall_waluigi
Enter the name of a comparable sound effect (metadata): vc_narration_characall_luigi
Added entry 112 to vc_narration_characall.nus3bank uwu

python sli_patch.py
Enter the filepath to soundlabelinfo.sli: soundlabelinfo.sli
Enter the new sound label: vc_narration_characall_waluigi
Enter the index of the new sound label in the NUS3Bank: 112
Enter a comparable sound label (from the same NUS3Bank): vc_narration_characall_luigi
Added sound label vc_narration_characall_waluigi ( 0x1efe26cfa6 ) to soundlabelinfo.sli owo
```

Example (BGM):
```
python nus3append.py
Enter the path of your file: bgm_crs2_42_crazyhand.nus3bank
Enter the name of the appended sound effect: force_addiction
Enter the name of a comparable sound effect (metadata): crs2_42_crazyhand
Added entry 1 to bgm_crs2_42_crazyhand.nus3bank uwu
```

There are other locations where you will have to add this information to the game. For example, when adding announcer calls you will have to add them to each character in `arc/ui/database/ui_chara_db.prc`. For more music tracks, I have no clue I didn't test that. CoolSonicKirby did though...
