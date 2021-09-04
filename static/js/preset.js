$(document).ready(function(){
    $.each(presets, function(preset, value){
        console.log(preset);
        $('#preset').append($("<option></option>").prop("value",preset).text(preset));
    })
    $('#preset').change(function(){
        setPreset(this.value);
    });

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("preset")){
        setPreset(urlParams.get("preset"));
    }
});



function setPreset(presetName){
    preset = parsePreset(presetName);
    console.log(preset);
    $('input').each(function(){
        $(this).prop("checked", false);
    });
    // preset['include'].forEach(location => $("input[value='".concat(location).concat("']")).prop("checked",true));
    $("input[type='checkbox']").each(function(){
        if(this.name in preset){
            $(this).prop("checked",preset[this.name].includes(this.value));
        }
    });
    $("input[type='number']").each(function(){
        if(this.name in preset){
            $(this).val(preset[this.name]);
        }
    });
    $("select").each(function(){
        if(this.name in preset){
            $(this).val(preset[this.name]).change();
        }
    });

    $('#starting-inventory option').each(function(){
        $(this).prop('selected',preset["starting-inventory"].includes(this.value));
    });
    tail.select('#starting-inventory').reload();




};

function parsePreset(option){
    if (presets[option]){
        return presets[option];
    }
    return JSON.parse(option);
}

const presets = {
    "League":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical"
        ],
        "levelChoice":"ExcludeFrom50",
        "keybladeMinStat":0,
        "keybladeMaxStat":7,
        "SoraExp":1.5,
        "ValorExp":5,
        "WisdomExp":3,
        "LimitExp":3,
        "MasterExp":2,
        "FinalExp":3,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"JSmartee",
        "PromiseCharm":[false],
        "starting-inventory":[]
    },
    "Escape STT":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.OCCups",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical"
        ],
        "levelChoice":"ExcludeFrom50",
        "keybladeMinStat":3,
        "keybladeMaxStat":10,
        "SoraExp":1.5,
        "ValorExp":5,
        "WisdomExp":3,
        "LimitExp":4,
        "MasterExp":3,
        "FinalExp":3,
        "keybladeAbilities":["Support","Action"],
        "enemy":"Disabled",
        "hintsType":"JSmartee",
        "PromiseCharm":[false],
        "starting-inventory":["537"]
    },
    "Cooperative":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical"
        ],
        "levelChoice":"ExcludeFrom50",
        "keybladeMinStat":0,
        "keybladeMaxStat":7,
        "SoraExp":1.5,
        "ValorExp":5,
        "WisdomExp":3,
        "LimitExp":3,
        "MasterExp":3,
        "FinalExp":3,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"Shananas",
        "PromiseCharm":[false],
        "starting-inventory":[]
    },
    "Beginner":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.AS"
        ],
        "levelChoice":"ExcludeFrom50",
        "keybladeMinStat":3,
        "keybladeMaxStat":10,
        "SoraExp":5,
        "ValorExp":5,
        "WisdomExp":5,
        "LimitExp":5,
        "MasterExp":5,
        "FinalExp":5,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"Shananas",
        "PromiseCharm":[false],
        "starting-inventory":[]
    },
    "Level 1":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.FormLevel",
            "locationType.Free",
        ],
        "levelChoice":"Level",
        "keybladeMinStat":0,
        "keybladeMaxStat":7,
        "SoraExp":1,
        "ValorExp":5,
        "WisdomExp":5,
        "LimitExp":5,
        "MasterExp":5,
        "FinalExp":5,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"Shananas",
        "PromiseCharm":[false],
        "starting-inventory":["404"]
    },
    "Bingo":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.OCCups",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical"
        ],
        "levelChoice":"Level",
        "keybladeMinStat":3,
        "keybladeMaxStat":10,
        "SoraExp":2.5,
        "ValorExp":6,
        "WisdomExp":4,
        "LimitExp":4,
        "MasterExp":3,
        "FinalExp":4,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"Shananas",
        "PromiseCharm":[false],
        "starting-inventory":[]
    },
    "Go Mode":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.OCCups",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical",
            "locationType.DataOrg",
            "locationType.LW"
        ],
        "levelChoice":"ExcludeFrom50",
        "keybladeMinStat":0,
        "keybladeMaxStat":7,
        "SoraExp":1.5,
        "ValorExp":5,
        "WisdomExp":3,
        "LimitExp":3,
        "MasterExp":3,
        "FinalExp":3,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"Shananas",
        "PromiseCharm":[false],
        "starting-inventory":["593","594","595"]
    },
    "Better All Blue Numbers":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical",
            "locationType.Atlantica",
            "locationType.LW",
            "locationType.DataOrg"
        ],
        "levelChoice":"ExcludeFrom99",
        "keybladeMinStat":5,
        "keybladeMaxStat":13,
        "SoraExp":7,
        "ValorExp":10,
        "WisdomExp":7,
        "LimitExp":7,
        "MasterExp":5,
        "FinalExp":7,
        "SummonExp":5,
        "keybladeAbilities":["Support", "Action"],
        "enemy":"Disabled",
        "hintsType":"Shananas",
        "PromiseCharm":[true],
        "starting-inventory":[],
        "seedModifiers": ["Schmovement", "Better Junk"]
    },
    "Community-Voted Settings (CVS)":{
        "include":[
            "locationType.LoD",
            "locationType.BC",
            "locationType.HB",
            "locationType.CoR",
            "locationType.TT",
            "locationType.TWTNW",
            "locationType.SP",
            "locationType.PR",
            "locationType.OC",
            "locationType.Agrabah",
            "locationType.HT",
            "locationType.PL",
            "locationType.DC",
            "locationType.HUNDREDAW",
            "locationType.STT",
            "locationType.AS",
            "locationType.Sephi",
            "locationType.DataOrg",
            "locationType.FormLevel",
            "locationType.Free",
            "locationType.Critical"
        ],
        "levelChoice":"ExcludeFrom50",
        "keybladeMinStat":3,
        "keybladeMaxStat":10,
        "SoraExp":1.5,
        "ValorExp":10,
        "WisdomExp":5,
        "LimitExp":5,
        "MasterExp":3,
        "FinalExp":5,
        "keybladeAbilities":["Support"],
        "enemy":"Disabled",
        "hintsType":"JSmartee",
        "PromiseCharm":[false],
        "starting-inventory":["138"]
    },
};
