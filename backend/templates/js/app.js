var counter = 0;
var first_name = '';
var fullname = '';
var email = '';
var modal_submit_register = 'Register';  
var modal_submit_password = 'Reset Password';  
var modal_submit_login    = 'Login';

// register modal component

Vue.config.devtools = true;

/*
Vue.transition('fade', {
    enterClass: 'fadeIn',
    leaveClass: 'fadeOut'
});

Vue.transition('fadeWithMove', {
    enterClass: 'fadeInDown',
    leaveClass: 'fadeOutUp'
});
*/

Vue.component('modal', {
  template: '#modal-template-signin',
  props: {
    show: {
      type: Boolean,
      required: true,
      twoWay: true
    }
  },
  methods: {
    close: function () {
        this.show = false;
    }
  },
  ready: function () {
    document.addEventListener("keydown", (e) => {
      if (this.show && e.keyCode == 27) {
        this.close();
      }
    });
  }

})



var qvm = new Vue({
  el: '#qualify-stepone',
  data: {
    state:'',
    is_spouse_location_known:'',
    are_there_children: '',
    does_spouse_agree:'',
    is_military:'',
  },
  methods: {
    submitone: function (event) {
              
               this.$set('is_spouse_location_known',$('#is_spouse_location_known').val());
               this.$set('are_there_children',$('#are_there_children').val());
               this.$set('does_spouse_agree',$('#does_spouse_agree').val());
               this.$set('is_military',$('#is_military').val());
               this.$set('state',$('#state-selected').val());
               $("#final-qualify-state").html("<h4><strong>"+$('#state-selected').val()+"</strong></h4>");

               if(!$('#is_spouse_location_known').is(":checked") || !$('#does_spouse_agree').is(":checked")) {
                      $('#final_does_qualify').html("<h4><strong>Congratulations! You qualify to use our contested divorce package!</strong></h4>");
               }          

               else {
                      $('#final_does_qualify').html("<h4><strong>Congratulations! You qualify to use our uncontested divorce package!</strong></h4>");
               }


    },
    submittwo: function (event) {
    },

    submitthree: function (event) {
    },

    submitfour: function (event) {
       alert('hi');
    },

    successCallback: function(event) {
            alert("SUCCESS");
    },
    errorCallback: function(event) {
            alert("ERROR");
    },
    validConfirm: function(event) {
           alert("VALID");
    }

  }
})


var qvm2 = new Vue({
  el: '#qualify-steptwo',
  data: {
    state:'',
    does_qualify:'',
    agree_to_start: '',
    is_spouse_location_known:'',
    are_there_children: '',
    does_spouse_agree:'',
    is_military:'',
  },
  methods: {
    submitone: function (event) {
           this.$set('does_qualify','NO');
           this.$set('state',$('#state-selected').val());
    },
    submittwo: function (event) {
    },

    submitthree: function (event) {
    },

    submitfour: function (event) {
         alert('hi hi');
    },

    successCallback: function(event) {
            alert("SUCCESS");
    },
    errorCallback: function(event) {
            alert("ERROR");
    },
    validConfirm: function(event) {
           alert("VALID");
    }
  },
  ready:function() {
      this.$set('does_qualify','NO');
      this.$set('state',$('#state-selected').val());

  }

})


var vm = new Vue({
  el: '#stepone',

  data: {
    email:'',
    phone:'',
    fullname: '',
  },

  methods: {

    submitone: function (event) {
               this.$set('phone',$('#phone').val());
               this.$set('email',$('#email').val());
               this.$set('fullname',$('#fullname').val());               
    },

    submittwo: function (event) {

    },

    submitthree: function (event) {
    },

    submitfour: function (event) {
        alert('hihihi');
    },

    successCallback: function(event) {
            alert("SUCCESS");
    },
    errorCallback: function(event) {
            alert("ERROR");
    },
    validConfirm: function(event) {
           alert("VALID");
    },
    ready:function() {
      this.$set('phone',$('#phone').val());
      this.$set('email',$('#email').val());
      this.$set('fullname',$('#fullname').val());
    }

    
  }
})


var vm2 = new Vue({
  el: '#steptwo',
  data: {
    email:'',
    phone:'',
    fullname: '',
    cardtype:'',
    cardnumber:'',
    expirationmonth:'',
    expirationyear:'',
  },
  methods: {
    submitone: function (event) {
    },
    submittwo: function (event) {
           this.$set('phone',vm.phone);
           this.$set('fullname',vm.fullname);
           vm3.$set('email',this.email);
           vm3.$set('fullname',this.fullname);
           vm3.$set('cardtype',this.cardtype);
           vm3.$set('cardnumber',this.cardnumber);
           vm3.$set('expirationmonth',this.expirationmonth);
           vm3.$set('expirationyear',this.expirationyear);
    },

    submitthree: function (event) {
    },

    submitfour: function (event) {
         alert('hi ho hi hi');
    },

    successCallback: function(event) {
            alert("SUCCESS");
    },
    errorCallback: function(event) {
            alert("ERROR");
    },
    validConfirm: function(event) {
           alert("VALID");
    }
  },
  ready:function() {
      this.$set('phone',vm.phone);  
      this.$set('email',$('#email').val());
      this.$set('fullname',$('#fullname').val());
    
  }
  
})



var vm3 = new Vue({
  el: '#stepthree',
  data: {
    email:'',
    fullname: '',
    address1: '',
    address2: '',
    city: '',
    state: '',
    zip:  '',
    phone: '2222',
    cardtype: '',
    cardnumber: '',
    expirationmonth: '',
    expirationyear: '',
  },
  methods: {
    submitone: function (event) {
    },
    submittwo: function (event) {
    },

    submitthree: function (event) {
               vm4.$set('email',this.email);
               vm4.$set('fullname',this.fullname);
               vm4.$set('cardtype',this.cardtype);
               vm4.$set('cardnumber',this.cardnumber);
               vm4.$set('expirationmonth',this.expirationmonth);
               vm4.$set('expirationyear',this.expirationyear);
               vm4.$set('address1',this.address1);
               vm4.$set('address2',this.address2); 
               vm4.$set('city',this.city);
               vm4.$set('state',this.state);
               vm4.$set('zip',this.zip);
               vm4.$set('phone',this.phone);  

               $("#phone").attr("value",this.phone.toString());
               $("#city").attr("value",this.city.toString());  
               $("#state").attr("value",this.state.toString());
               $("#zip").attr("value",this.zip.toString());
               $("#month").attr("value",this.expirationmonth.toString());
               $("#year").attr("value",this.expirationyear.toString());
               $("#email").attr("value",this.email.toString());
               $("#fullname").attr("value",this.fullname.toString());
               $("#cardtype").attr("value",this.cardtype.toString());
               $("#cardnumber").attr("value",this.cardnumber.toString());
               $("#address1").attr("value",this.address1.toString());  
               $("#address2").attr("value",this.address2.toString());

               $("#final_email").html("<p><strong>Email: "+this.email.toString()+"</strong></p>");
               $("#final_phone").html("<p><strong>Phone: "+this.phone.toString()+"</strong></p>");
               $("#final_fullname").html("<p><strong>Full Name: "+this.fullname.toString()+"</strong></p>");   
               $("#final_cardtype").html("<p><strong>Card Type: "+this.cardtype.toString()+"</strong></p>");  
               $("#final_cardnumber").html("<p><strong>Card Number: "+this.cardnumber.toString()+"</strong></p>");   
               $("#final_expirationmonth").html("<p><strong>Expiration Month: "+this.expirationmonth.toString()+"</strong></p>");
               $("#final_expirationyear").html("<p><strong>Expiration Year: "+this.expirationyear.toString()+"</strong></p>");   
               $("#final_address1").html("<p><strong>Address 1: "+this.address1.toString()+"</strong></p>");   
               $("#final_address2").html("<p><strong>Address 2: "+this.address2.toString()+"</strong></p>"); 
               $("#final_city").html("<p><strong>City: "+this.city.toString()+"</strong></p>");
               $("#final_state").html("<p><strong>State: "+this.state.toString()+"</strong></p>");  
               $("#final_zip").html("<p><strong>Zip Code: "+this.zip.toString()+"</strong></p>");
    },

    submitfour: function (event) {
          alert('hi hi hi hi hi');
    },

    successCallback: function(event) {
            alert("SUCCESS");
    },
    errorCallback: function(event) {
            alert("ERROR");
    },
    validConfirm: function(event) {
           alert("VALID");
    }

  },
  ready: function() {
           this.phone=vm2.phone;
  }
})


var vm4 = new Vue({
  el: '#stepfour',
  data: {
     
    email:vm3.email,
    fullname: vm3.fullname,
    address1: vm3.address1,
    address2: vm3.address2,
    city: vm3.city,
    state: vm3.state,
    zip:  vm3.zip,
    phone: '393-342-4232',
    cardtype: vm3.cardtype,
    cardnumber: vm3.cardnumber,
    expirationmonth: vm3.expirationmonth,
    expirationyear: vm3.expirationyear,
  },
  // define methods under the `methods` object
  methods: {

    submitone: function (event) {
    },

    submittwo: function (event) {
    },

    submitthree: function (event) {
    },

    submitfour: function (event) {
    },

    successCallback: function(event) {
    },

    errorCallback: function(event) {
    },

    validConfirm: function(event) {
    }

  },
  ready:function() {
  }
})


var vm5 = new Vue({
  el: '#stepfive',
  data: {
    email:vm3.email,
    phone:vm3.phone,
    fullname: vm3.fullname,
    address1: '',
    address2: '',
    city: '',
    state: '',
    zip:  '',
    cardtype: '',
    cardnumber: '',
    expirationmonth: '',
    expirationyear: '',
  },
  // define methods under the `methods` object
  methods: {

    submitone: function (event) {
    },

    submittwo: function (event) {
    },

    submitthree: function (event) {
    },

    submitfour: function (event) {
            alert('hi hi hi hi hi hi');
    },

    submitfive: function (event) {
         alert('pay');
    },
    successCallback: function(event) {
    },

    errorCallback: function(event) {
    },

    validConfirm: function(event) {
    }

  },
  ready:function() {
  }
})


// start app
new Vue({
  el: '#contactus',
  data: {
      name:'',
      email:'',
      phone:'',
      message:'',
  },
  options: {
  },
  methods: {
     successCallback: function() {
            alert("SUCCESS");
     },
     errorCallback: function() {
            alert("ERROR");
     },
     validConfirm: function() {
           alert("VALID");
           $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
     },
     submit: function() {
         $.get('http://divorcesus.com/sendmail?email='+this.email+'&phone='+this.phone+'&message='+this.message+'&name='+this.name, function(data)
                {
                     if (data.message =='success')  {
                          
                           $( "div.success" ).fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );       
                     }
                    this.$set('email','');
                    this.$set('phone','');
                    this.$set('message','');
                    this.$set('name','');
                });
     }
  }
})

new Vue({
  el: '#main_wrapper',
  data: {
    showModal: false,
    showNewCommentModal: false,
    active: null,
  },
  methods: {
    open: function(which, e) {
      // Prevents clicking the link from doing anything
        e.preventDefault();
        modal.active = which;
    },
    close: function (e) {
    },
    submit: function(which, e) {
            e.preventDefault();
    }


  },

  ready: function () {
  }

})


Vue.component('NewCommentModal', {
  template: '#new-comment-modal-template',
  props: ['show'],
  data: function () {
  	return {
      comment: ''
    };
  },
  methods: {
    close: function () {
      this.show = false;
      this.comment = '';
    },
    postComment: function () {
      // Insert AJAX call here...
      this.close();
    }
  }
})

new Vue({
  el: '#app',
  data: {
    showModal: false,
    showNewCommentModal: false,
    active: null,
  },
  methods: {
    open: function(which, e) {
      // Prevents clicking the link from doing anything
        e.preventDefault();
        modal.active = which;
    },
    close: function (e) {
    },
    submit: function(which, e) {
            e.preventDefault();
    },
    signout: function(which, e) {
        alert('signout');
    }

  },
  create: function () {
      alert("REDY");
  },
  ready: function () {
      alert("READY");
  }

});


