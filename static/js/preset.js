$(document).ready(function(){
    $.each(presets, function(preset, value){
        console.log(preset);
        $('#preset').append($("<option></option>").prop("value",preset).text(preset));
    })
    $('#preset').change(function(){
        setPreset(this.value);
    });
});


function setPreset(presetName){
    preset = presets[presetName];
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
        if (preset["starting-inventory"].includes(this.value)){
            $(this).prop('selected',true);
        }
        else{
            $(this).prop('selected',false);
        }
    });
    $('#starting-inventory').multiselect('refresh');




};

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
    }
};