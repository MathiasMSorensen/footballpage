(function() {
  var $closeBtn, $heading, $loadBtn, $loading, $players, $playersAway, $playersHome, $stage, $subHeading, $switchBtn, $switcher, $team, $teamListHome, $terrain, $world, ASSET_URL, anim, data, dom, events, init, pos, scenes, state;

  ASSET_URL = 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/215059/';

  $stage = null;

  $world = null;

  $terrain = null;

  $team = null;

  $teamListHome = null;

  $players = null;

  $playersHome = null; // Subset of $players

  $playersAway = null; // Subset of $players

  $switchBtn = null;

  $loadBtn = null;

  $closeBtn = null;

  $heading = null;

  $subHeading = null;

  $loading = null;

  $switcher = null;

  data = {
    players: {
      home: [
        {
          name: 'Pizarro',
          asset: 'bm-pizarro.jpg',
          origin: 'Peru',
          height: '1.84m',
          shirt: '14',
          pos: 'Forward',
          dob: '36',
          goals: 1,
          games: 16,
          x: 110,
          y: -190
        },
        {
          name: 'Robben',
          asset: 'bm-robben.png',
          origin: 'Holland',
          height: '1.80m',
          shirt: '10',
          pos: 'Forward',
          dob: '32',
          goals: 19,
          games: 30,
          x: -110,
          y: -190
        },
        {
          name: 'Rilbery',
          asset: 'bm-rilbery.jpg',
          origin: 'France',
          height: '1.70m',
          shirt: '7',
          pos: 'Midfield',
          dob: '32',
          goals: 9,
          games: 22,
          x: 150,
          y: 50
        },
        {
          name: 'Schweinsteiger',
          asset: 'bm-schweinsteiger.jpg',
          origin: 'Germany',
          height: '1.87m',
          shirt: '24',
          pos: 'Forward',
          dob: '31',
          goals: 21,
          games: 3,
          x: 0,
          y: 100
        },
        {
          name: 'Martinez',
          asset: 'bm-martinez.jpg',
          origin: 'Spain',
          height: '1.90m',
          shirt: '8',
          pos: 'Midfield',
          dob: '28',
          goals: 0,
          games: 2,
          x: -150,
          y: 50
        },
        {
          name: 'Alaba',
          asset: 'bm-alaba.jpg',
          origin: 'Austria',
          height: '1.80m',
          shirt: '27',
          pos: 'Defence',
          dob: '24',
          goals: 5,
          games: 27,
          x: -200,
          y: 180
        },
        {
          name: 'Lahm',
          asset: 'bm-lahm.jpg',
          origin: 'Germany',
          height: '1.70',
          shirt: '21',
          pos: 'Defence',
          dob: '32',
          goals: 2,
          games: 25,
          x: 200,
          y: 180
        },
        {
          name: 'Benatia',
          asset: 'bm-benatia.jpg',
          origin: 'France',
          height: '1.87m',
          shirt: '5',
          pos: 'Defence',
          dob: '31',
          goals: 21,
          games: 1,
          x: 100,
          y: 300
        },
        {
          name: 'Dante',
          asset: 'bm-dante.jpg',
          origin: 'Brazil',
          height: '1.87m',
          shirt: '4',
          pos: 'Defence',
          dob: '32',
          goals: 0,
          games: 34,
          x: -100,
          y: 300
        },
        {
          name: 'Neuer',
          asset: 'bm-neuer.jpg',
          origin: 'Germany',
          height: '1.93m',
          shirt: '1',
          pos: 'Goalie',
          dob: '29',
          goals: 0,
          games: 48,
          x: 0,
          y: 410
        }
      ],
      away: [
        {
          name: 'Benzema',
          asset: 'rm-benzema.jpg',
          origin: 'France',
          height: '1.87m',
          shirt: '9',
          pos: 'Forward',
          dob: '36',
          goals: 1,
          games: 16,
          x: 110,
          y: -190
        },
        {
          name: 'Bale',
          asset: 'rm-bale.jpg',
          origin: 'Wales',
          height: '1.83m',
          shirt: '11',
          pos: 'Midfield',
          dob: '26',
          goals: 19,
          games: 30,
          x: -110,
          y: -190
        },
        {
          name: 'carvajal',
          asset: 'rm-carvajal.jpg',
          origin: 'Spain',
          height: '1.70m',
          shirt: '15',
          pos: 'Defender',
          dob: '32',
          goals: 9,
          games: 22,
          x: 150,
          y: 50
        },
        {
          name: 'Silva',
          asset: 'rm-silva.jpg',
          origin: 'Brazil',
          height: '1.87m',
          shirt: '16',
          pos: 'Forward',
          dob: '22',
          goals: 21,
          games: 3,
          x: 0,
          y: 100
        },
        {
          name: 'Kroos',
          asset: 'rm-kroos.jpg',
          origin: 'Germany',
          height: '1.82',
          shirt: '8',
          pos: 'Midfield',
          dob: '25',
          goals: 0,
          games: 2,
          x: -150,
          y: 50
        },
        {
          name: 'Modric',
          asset: 'rm-modric.jpg',
          origin: 'Croatia',
          height: '1.74m',
          shirt: '19',
          pos: 'Midfield',
          dob: '30',
          goals: 5,
          games: 27,
          x: -200,
          y: 180
        },
        {
          name: 'Nacho',
          asset: 'rm-nacho.jpg',
          origin: 'Germany',
          height: '1.79',
          shirt: '18',
          pos: 'Defence',
          dob: '25',
          goals: 2,
          games: 25,
          x: 200,
          y: 180
        },
        {
          name: 'Ramos',
          asset: 'rm-ramos.jpg',
          origin: 'Spain',
          height: '1.83m',
          shirt: '4',
          pos: 'Defence',
          dob: '31',
          goals: 21,
          games: 1,
          x: 100,
          y: 300
        },
        {
          name: 'Pepe',
          asset: 'rm-pepe.jpg',
          origin: 'Brazil',
          height: '1.88m',
          shirt: '3',
          pos: 'Defence',
          dob: '32',
          goals: 0,
          games: 34,
          x: -100,
          y: 300
        },
        {
          name: 'Casillas',
          asset: 'rm-casillas.jpg',
          origin: 'Spain',
          height: '1.85m',
          shirt: '1',
          pos: 'Goalie',
          dob: '34',
          goals: 0,
          games: 48,
          x: 0,
          y: 410
        }
      ]
    }
  };

  state = {
    home: true,
    disabHover: false,
    swapSides: function() {
      if (this.home) {
        return this.home = false;
      } else {
        return this.home = true;
      }
    },
    curSide: function() {
      if (this.home) {
        return 'home';
      } else {
        return 'away';
      }
    }
  };

  pos = {
    world: {
      baseX: 0,
      baseY: 0,
      baseZ: -200
    },
    def: {
      goalie: [0, -50]
    }
  };

  dom = {
    addPlayers: function(side) {
      var $el, key, ref, val;
      ref = data.players[side];
      for (key in ref) {
        val = ref[key];
        val.side = side;
        $el = this.addPlayer(val);
        $team.append($el);
      }
      $players = $('.js-player');
      $playersHome = $('.js-player[data-side="home"]');
      return $playersAway = $('.js-player[data-side="away"]');
    },
    addPlayer: function(data) {
      var $el;
      $el = $('<div class="js-player player" data-name="' + data.name + '" data-side="' + data.side + '" data-x="' + data.x + '" data-y="' + data.y + '"></div>');
      $el.append('<div class="player__label"><span>' + data.name + '</span></div>');
      $el.append('<div class="player__img"><img src= ' + ASSET_URL + data.asset + '></div>');
      $el.prepend('<div class="player__card"> </div>');
      $el.prepend('<div class="player__placeholder"></div>');
      this.populateCard($el.find('.player__card'), data);
      return $el;
    },
    preloadImages: function(preload) {
      var i, promises;
      promises = [];
      i = 0;
      while (i < preload.length) {
        (function(url, promise) {
          var img;
          img = new Image();
          img.onload = function() {
            return promise.resolve();
          };
          return img.src = url;
        })(preload[i], promises[i] = $.Deferred());
        i++;
      }
      return $.when.apply($, promises).done(function() {
        scenes.endLoading();
        return scenes.loadIn(1600);
      });
    },
    populateCard: function($el, data) {
      return $el.append('<h3>' + data.name + '</h3>' + '<ul class="player__card__list"><li><span>DOB</span><br/>' + data.dob + ' yr</li><li><span>Height</span><br/>' + data.height + '</li><li><span>Origin</span><br/>' + data.origin + '</li></ul>' + '<ul class="player__card__list player__card__list--last"><li><span>Games</span><br/>' + data.games + '</li><li><span>Goals</span><br/>' + data.goals + '</li></ul>');
    },
    displayNone: function($el) {
      return $el.css('display', 'none');
    }
  };

  events = {
    attachAll: function() {
      $switchBtn.on('click', function(e) {
        var $el;
        e.preventDefault();
        $el = $(this);
        if ($el.hasClass('disabled')) {
          return;
        }
        scenes.switchSides();
        $switchBtn.removeClass('disabled');
        return $el.addClass('disabled');
      });
      $loadBtn.on('click', function(e) {
        e.preventDefault();
        return scenes.loadIn();
      });
      return $players.on('click', function(e) {
        var $el;
        e.preventDefault();
        $el = $(this);
        if ($('.active').length) {
          return false;
        }
        $el.addClass('active');
        scenes.focusPlayer($el);
        return setTimeout((function() {
          return events.attachClose();
        }), 1);
      });
    },
    attachClose: function() {
      return $stage.one('click', function(e) {
        e.preventDefault();
        return scenes.unfocusPlayer();
      });
    }
  };

  scenes = {
    preLoad: function() {
      $teamListHome.velocity({
        opacity: 0
      }, 0);
      $players.velocity({
        opacity: 0
      }, 0);
      $loadBtn.velocity({
        opacity: 0
      }, 0);
      $switcher.velocity({
        opacity: 0
      }, 0);
      $heading.velocity({
        opacity: 0
      }, 0);
      $subHeading.velocity({
        opacity: 0
      }, 0);
      $playersAway.css('display', 'none');
      $world.velocity({
        opacity: 0,
        translateZ: -200,
        translateY: -60
      }, 0);
      return $('main').velocity({
        opacity: 1
      }, 0);
    },
    loadIn: function(delay = 0) {
      var delayInc;
      $world.velocity({
        opacity: 1,
        translateY: 0,
        translateZ: -200
      }, {
        duration: 1000,
        delay: delay,
        easing: 'spring'
      });
      anim.fadeInDir($heading, 300, delay + 600, 0, 30);
      anim.fadeInDir($subHeading, 300, delay + 800, 0, 30);
      anim.fadeInDir($teamListHome, 300, delay + 800, 0, 30);
      anim.fadeInDir($switcher, 300, delay + 900, 0, 30);
      delay += 1200;
      delayInc = 30;
      return anim.dropPlayers($playersHome, delay, delayInc);
    },
    startLoading: function() {
      var images, key, ref, val;
      anim.fadeInDir($loading, 300, 0, 0, -20);
      images = [];
      ref = data.players.home && data.players.away;
      for (key in ref) {
        val = ref[key];
        images.push(ASSET_URL + val.asset);
      }
      return dom.preloadImages(images);
    },
    endLoading: function() {
      return anim.fadeOutDir($loading, 300, 1000, 0, -20);
    },
    arrangePlayers: function() {
      return $players.each(function() {
        var $el;
        $el = $(this);
        return $el.velocity({
          translateX: parseInt($el.attr('data-x')),
          translateZ: parseInt($el.attr('data-y')) // Z is the Y axis on the field
        });
      });
    },
    focusPlayer: function($el) {
      var shiftY;
      data = $el.data();
      shiftY = data.y;
      if (shiftY > 0) {
        shiftY = data.y / 2;
      }
      $('.js-player[data-side="' + state.curSide() + '"]').not('.active').each(function() {
        var $unfocus;
        $unfocus = $(this);
        return anim.fadeOutDir($unfocus, 300, 0, 0, 0, 0, null, 0.2);
      });
      $world.velocity({
        translateX: pos.world.baseX - data.x,
        translateY: pos.world.baseY,
        translateZ: pos.world.baseZ - shiftY // Z is the Y axis on the field
      }, 600);
      $terrain.velocity({
        opacity: 0.66
      }, 600);
      return this.showPlayerCard($el, 600, 600);
    },
    unfocusPlayer: function() {
      var $el;
      $el = $('.js-player.active');
      data = $el.data();
      anim.fadeInDir($('.js-player[data-side="' + state.curSide() + '"]').not('.active'), 300, 300, 0, 0, 0, null, 0.2);
      $el.removeClass('active');
      $world.velocity({
        translateX: pos.world.baseX,
        translateY: pos.world.baseY,
        translateZ: pos.world.baseZ // Z is the Y axis on the field
      }, 600);
      $terrain.velocity({
        opacity: 1
      }, 600);
      return this.hidePlayerCard($el, 600, 600);
    },
    hidePlayerCard: function($el, dur, delay) {
      var $card, $image;
      $card = $el.find('.player__card');
      $image = $el.find('.player__img');
      $image.velocity({
        translateY: 0
      }, 300);
      anim.fadeInDir($el.find('.player__label', 200, delay));
      return anim.fadeOutDir($card, 300, 0, 0, -100);
    },
    showPlayerCard: function($el, dur, delay) {
      var $card, $image;
      $card = $el.find('.player__card');
      $image = $el.find('.player__img');
      $image.velocity({
        translateY: '-=150px'
      }, 300);
      anim.fadeOutDir($el.find('.player__label', 200, delay));
      return anim.fadeInDir($card, 300, 200, 0, 100);
    },
    switchSides: function() {
      var $new, $old, delay, delayInc;
      delay = 0;
      delayInc = 20;
      $old = $playersHome;
      $new = $playersAway;
      if (!state.home) {
        $old = $playersAway;
        $new = $playersHome;
      }
      state.swapSides();
      $old.each(function() {
        var $el;
        $el = $(this);
        anim.fadeOutDir($el, 200, delay, 0, -60, 0);
        anim.fadeOutDir($el.find('.player__label'), 200, delay + 700);
        return delay += delayInc;
      });
      $terrain.velocity({
        rotateY: '+=180deg'
      }, {
        delay: 150,
        duration: 1200
      });
      return anim.dropPlayers($new, 1500, 30);
    }
  };

  anim = {
    fadeInDir: function($el, dur, delay, deltaX = 0, deltaY = 0, deltaZ = 0, easing = null, opacity = 0) {
      $el.css('display', 'block');
      $el.velocity({
        translateX: '-=' + deltaX,
        translateY: '-=' + deltaY,
        translateZ: '-=' + deltaZ
      }, 0);
      return $el.velocity({
        opacity: 1,
        translateX: '+=' + deltaX,
        translateY: '+=' + deltaY,
        translateZ: '+=' + deltaZ
      }, {
        easing: easing,
        delay: delay,
        duration: dur
      });
    },
    fadeOutDir: function($el, dur, delay, deltaX = 0, deltaY = 0, deltaZ = 0, easing = null, opacity = 0) {
      var display;
      if (!opacity) {
        display = 'none';
      } else {
        display = 'block';
      }
      return $el.velocity({
        opacity: opacity,
        translateX: '+=' + deltaX,
        translateY: '+=' + deltaY,
        translateZ: '+=' + deltaZ
      }, {
        easing: easing,
        delay: delay,
        duration: dur
      }).velocity({
        opacity: opacity,
        translateX: '-=' + deltaX,
        translateY: '-=' + deltaY,
        translateZ: '-=' + deltaZ
      }, {
        duration: 0,
        display: display
      });
    },
    dropPlayers: function($els, delay, delayInc) {
      return $els.each(function() {
        var $el;
        $el = $(this);
        $el.css({
          display: 'block',
          opacity: 0
        });
        anim.fadeInDir($el, 800, delay, 0, 50, 0, 'spring');
        anim.fadeInDir($el.find('.player__label'), 200, delay + 250);
        return delay += delayInc;
      });
    }
  };

  init = function() {
    $stage = $('.js-stage');
    $world = $('.js-world');
    $switchBtn = $('.js-switch');
    $loadBtn = $('.js-load');
    $heading = $('.js-heading');
    $switcher = $('.js-switcher');
    $closeBtn = $('.js-close');
    $subHeading = $('.js-subheading');
    $terrain = $('.js-terrain');
    $team = $('.js-team');
    $teamListHome = $('.js-team-home');
    $loading = $('.js-loading');
    dom.addPlayers('home');
    dom.addPlayers('away');
    scenes.preLoad();
    scenes.arrangePlayers();
    events.attachAll();
    return scenes.startLoading();
  };

  $(document).ready(function() {
    return init();
  });

}).call(this);

//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiPGFub255bW91cz4iXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7QUFBQSxNQUFBLFNBQUEsRUFBQSxRQUFBLEVBQUEsUUFBQSxFQUFBLFFBQUEsRUFBQSxRQUFBLEVBQUEsWUFBQSxFQUFBLFlBQUEsRUFBQSxNQUFBLEVBQUEsV0FBQSxFQUFBLFVBQUEsRUFBQSxTQUFBLEVBQUEsS0FBQSxFQUFBLGFBQUEsRUFBQSxRQUFBLEVBQUEsTUFBQSxFQUFBLFNBQUEsRUFBQSxJQUFBLEVBQUEsSUFBQSxFQUFBLEdBQUEsRUFBQSxNQUFBLEVBQUEsSUFBQSxFQUFBLEdBQUEsRUFBQSxNQUFBLEVBQUE7O0VBQUEsU0FBQSxHQUFZOztFQUVaLE1BQUEsR0FBZ0I7O0VBQ2hCLE1BQUEsR0FBZ0I7O0VBQ2hCLFFBQUEsR0FBZ0I7O0VBQ2hCLEtBQUEsR0FBZ0I7O0VBQ2hCLGFBQUEsR0FBZ0I7O0VBQ2hCLFFBQUEsR0FBZ0I7O0VBQ2hCLFlBQUEsR0FBZ0IsS0FSaEI7O0VBU0EsWUFBQSxHQUFnQixLQVRoQjs7RUFVQSxVQUFBLEdBQWdCOztFQUNoQixRQUFBLEdBQWdCOztFQUNoQixTQUFBLEdBQWdCOztFQUNoQixRQUFBLEdBQWdCOztFQUNoQixXQUFBLEdBQWdCOztFQUNoQixRQUFBLEdBQWdCOztFQUNoQixTQUFBLEdBQWdCOztFQUVoQixJQUFBLEdBQ0k7SUFBQSxPQUFBLEVBQ0k7TUFBQSxJQUFBLEVBQU07UUFDRjtVQUFFLElBQUEsRUFBTSxTQUFSO1VBQW1CLEtBQUEsRUFBTyxnQkFBMUI7VUFBNEMsTUFBQSxFQUFRLE1BQXBEO1VBQTRELE1BQUEsRUFBUSxPQUFwRTtVQUE2RSxLQUFBLEVBQU8sSUFBcEY7VUFBMEYsR0FBQSxFQUFLLFNBQS9GO1VBQTBHLEdBQUEsRUFBSyxJQUEvRztVQUFxSCxLQUFBLEVBQU8sQ0FBNUg7VUFBK0gsS0FBQSxFQUFPLEVBQXRJO1VBQTBJLENBQUEsRUFBRyxHQUE3STtV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LENBQUMsS0FBWixDQUFrQixRQUFBLENBQUEsQ0FBQTtXQUNkLElBQUEsQ0FBQTtFQURjLENBQWxCO0FBM1VBIiwic291cmNlc0NvbnRlbnQiOlsiQVNTRVRfVVJMID0gJ2h0dHBzOi8vczMtdXMtd2VzdC0yLmFtYXpvbmF3cy5jb20vcy5jZHBuLmlvLzIxNTA1OS8nXG5cbiRzdGFnZSAgICAgICAgPSBudWxsXG4kd29ybGQgICAgICAgID0gbnVsbFxuJHRlcnJhaW4gICAgICA9IG51bGxcbiR0ZWFtICAgICAgICAgPSBudWxsXG4kdGVhbUxpc3RIb21lID0gbnVsbFxuJHBsYXllcnMgICAgICA9IG51bGxcbiRwbGF5ZXJzSG9tZSAgPSBudWxsICMgU3Vic2V0IG9mICRwbGF5ZXJzXG4kcGxheWVyc0F3YXkgID0gbnVsbCAjIFN1YnNldCBvZiAkcGxheWVyc1xuJHN3aXRjaEJ0biAgICA9IG51bGxcbiRsb2FkQnRuICAgICAgPSBudWxsXG4kY2xvc2VCdG4gICAgID0gbnVsbFxuJGhlYWRpbmcgICAgICA9IG51bGxcbiRzdWJIZWFkaW5nICAgPSBudWxsXG4kbG9hZGluZyAgICAgID0gbnVsbFxuJHN3aXRjaGVyICAgICA9IG51bGxcblxuZGF0YSA9XG4gICAgcGxheWVyczpcbiAgICAgICAgaG9tZTogW1xuICAgICAgICAgICAgeyBuYW1lOiAnUGl6YXJybycsIGFzc2V0OiAnYm0tcGl6YXJyby5qcGcnLCBvcmlnaW46ICdQZXJ1JywgaGVpZ2h0OiAnMS44NG0nLCBzaGlydDogJzE0JywgcG9zOiAnRm9yd2FyZCcsIGRvYjogJzM2JywgZ29hbHM6IDEsIGdhbWVzOiAxNiwgeDogMTEwLCB5OiAtMTkwIH1cbiAgICAgICAgICAgIHsgbmFtZTogJ1JvYmJlbicsIGFzc2V0OiAnYm0tcm9iYmVuLnBuZycsIG9yaWdpbjogJ0hvbGxhbmQnLCBoZWlnaHQ6ICcxLjgwbScsIHNoaXJ0OiAnMTAnLCBwb3M6ICdGb3J3YXJkJywgZG9iOiAnMzInLCBnb2FsczogMTksIGdhbWVzOiAzMCwgeDogLTExMCwgeTogLTE5MCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdSaWxiZXJ5JywgYXNzZXQ6ICdibS1yaWxiZXJ5LmpwZycsIG9yaWdpbjogJ0ZyYW5jZScsIGhlaWdodDogJzEuNzBtJywgc2hpcnQ6ICc3JywgcG9zOiAnTWlkZmllbGQnLCBkb2I6ICczMicsIGdvYWxzOiA5LCBnYW1lczogMjIsIHg6IDE1MCwgeTogNTAgfVxuICAgICAgICAgICAgeyBuYW1lOiAnU2Nod2VpbnN0ZWlnZXInLCBhc3NldDogJ2JtLXNjaHdlaW5zdGVpZ2VyLmpwZycsIG9yaWdpbjogJ0dlcm1hbnknLCBoZWlnaHQ6ICcxLjg3bScsIHNoaXJ0OiAnMjQnLCBwb3M6ICdGb3J3YXJkJywgZG9iOiAnMzEnLCBnb2FsczogMjEsIGdhbWVzOiAzLCB4OiAwLCB5OiAxMDAgfVxuICAgICAgICAgICAgeyBuYW1lOiAnTWFydGluZXonLCBhc3NldDogJ2JtLW1hcnRpbmV6LmpwZycsIG9yaWdpbjogJ1NwYWluJywgaGVpZ2h0OiAnMS45MG0nLCBzaGlydDogJzgnLCBwb3M6ICdNaWRmaWVsZCcsIGRvYjogJzI4JywgZ29hbHM6IDAsIGdhbWVzOiAyLCB4OiAtMTUwLCB5OiA1MCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdBbGFiYScsIGFzc2V0OiAnYm0tYWxhYmEuanBnJywgb3JpZ2luOiAnQXVzdHJpYScsIGhlaWdodDogJzEuODBtJywgc2hpcnQ6ICcyNycsIHBvczogJ0RlZmVuY2UnLCBkb2I6ICcyNCcsIGdvYWxzOiA1LCBnYW1lczogMjcsIHg6IC0yMDAsIHk6IDE4MCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdMYWhtJywgYXNzZXQ6ICdibS1sYWhtLmpwZycsIG9yaWdpbjogJ0dlcm1hbnknLCBoZWlnaHQ6ICcxLjcwJywgc2hpcnQ6ICcyMScsIHBvczogJ0RlZmVuY2UnLCBkb2I6ICczMicsIGdvYWxzOiAyLCBnYW1lczogMjUsIHg6IDIwMCwgeTogMTgwIH1cbiAgICAgICAgICAgIHsgbmFtZTogJ0JlbmF0aWEnLCBhc3NldDogJ2JtLWJlbmF0aWEuanBnJywgb3JpZ2luOiAnRnJhbmNlJywgaGVpZ2h0OiAnMS44N20nLCBzaGlydDogJzUnLCBwb3M6ICdEZWZlbmNlJywgZG9iOiAnMzEnLCBnb2FsczogMjEsIGdhbWVzOiAxLCB4OiAxMDAsIHk6IDMwMCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdEYW50ZScsIGFzc2V0OiAnYm0tZGFudGUuanBnJywgb3JpZ2luOiAnQnJhemlsJywgaGVpZ2h0OiAnMS44N20nLCBzaGlydDogJzQnLCBwb3M6ICdEZWZlbmNlJywgZG9iOiAnMzInLCBnb2FsczogMCwgZ2FtZXM6IDM0LCB4OiAtMTAwLCB5OiAzMDAgfVxuICAgICAgICAgICAgeyBuYW1lOiAnTmV1ZXInLCBhc3NldDogJ2JtLW5ldWVyLmpwZycsIG9yaWdpbjogJ0dlcm1hbnknLCBoZWlnaHQ6ICcxLjkzbScsIHNoaXJ0OiAnMScsIHBvczogJ0dvYWxpZScsIGRvYjogJzI5JywgZ29hbHM6IDAsIGdhbWVzOiA0OCwgeDogMCwgeTogNDEwIH1cbiAgICAgICAgXVxuICAgICAgICBhd2F5OiBbXG4gICAgICAgICAgICB7IG5hbWU6ICdCZW56ZW1hJywgYXNzZXQ6ICdybS1iZW56ZW1hLmpwZycsIG9yaWdpbjogJ0ZyYW5jZScsIGhlaWdodDogJzEuODdtJywgc2hpcnQ6ICc5JywgcG9zOiAnRm9yd2FyZCcsIGRvYjogJzM2JywgZ29hbHM6IDEsIGdhbWVzOiAxNiwgeDogMTEwLCB5OiAtMTkwIH1cbiAgICAgICAgICAgIHsgbmFtZTogJ0JhbGUnLCBhc3NldDogJ3JtLWJhbGUuanBnJywgb3JpZ2luOiAnV2FsZXMnLCBoZWlnaHQ6ICcxLjgzbScsIHNoaXJ0OiAnMTEnLCBwb3M6ICdNaWRmaWVsZCcsIGRvYjogJzI2JywgZ29hbHM6IDE5LCBnYW1lczogMzAsIHg6IC0xMTAsIHk6IC0xOTAgfVxuICAgICAgICAgICAgeyBuYW1lOiAnY2FydmFqYWwnLCBhc3NldDogJ3JtLWNhcnZhamFsLmpwZycsIG9yaWdpbjogJ1NwYWluJywgaGVpZ2h0OiAnMS43MG0nLCBzaGlydDogJzE1JywgcG9zOiAnRGVmZW5kZXInLCBkb2I6ICczMicsIGdvYWxzOiA5LCBnYW1lczogMjIsIHg6IDE1MCwgeTogNTAgfVxuICAgICAgICAgICAgeyBuYW1lOiAnU2lsdmEnLCBhc3NldDogJ3JtLXNpbHZhLmpwZycsIG9yaWdpbjogJ0JyYXppbCcsIGhlaWdodDogJzEuODdtJywgc2hpcnQ6ICcxNicsIHBvczogJ0ZvcndhcmQnLCBkb2I6ICcyMicsIGdvYWxzOiAyMSwgZ2FtZXM6IDMsIHg6IDAsIHk6IDEwMCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdLcm9vcycsIGFzc2V0OiAncm0ta3Jvb3MuanBnJywgb3JpZ2luOiAnR2VybWFueScsIGhlaWdodDogJzEuODInLCBzaGlydDogJzgnLCBwb3M6ICdNaWRmaWVsZCcsIGRvYjogJzI1JywgZ29hbHM6IDAsIGdhbWVzOiAyLCB4OiAtMTUwLCB5OiA1MCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdNb2RyaWMnLCBhc3NldDogJ3JtLW1vZHJpYy5qcGcnLCBvcmlnaW46ICdDcm9hdGlhJywgaGVpZ2h0OiAnMS43NG0nLCBzaGlydDogJzE5JywgcG9zOiAnTWlkZmllbGQnLCBkb2I6ICczMCcsIGdvYWxzOiA1LCBnYW1lczogMjcsIHg6IC0yMDAsIHk6IDE4MCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdOYWNobycsIGFzc2V0OiAncm0tbmFjaG8uanBnJywgb3JpZ2luOiAnR2VybWFueScsIGhlaWdodDogJzEuNzknLCBzaGlydDogJzE4JywgcG9zOiAnRGVmZW5jZScsIGRvYjogJzI1JywgZ29hbHM6IDIsIGdhbWVzOiAyNSwgeDogMjAwLCB5OiAxODAgfVxuICAgICAgICAgICAgeyBuYW1lOiAnUmFtb3MnLCBhc3NldDogJ3JtLXJhbW9zLmpwZycsIG9yaWdpbjogJ1NwYWluJywgaGVpZ2h0OiAnMS44M20nLCBzaGlydDogJzQnLCBwb3M6ICdEZWZlbmNlJywgZG9iOiAnMzEnLCBnb2FsczogMjEsIGdhbWVzOiAxLCB4OiAxMDAsIHk6IDMwMCB9XG4gICAgICAgICAgICB7IG5hbWU6ICdQZXBlJywgYXNzZXQ6ICdybS1wZXBlLmpwZycsIG9yaWdpbjogJ0JyYXppbCcsIGhlaWdodDogJzEuODhtJywgc2hpcnQ6ICczJywgcG9zOiAnRGVmZW5jZScsIGRvYjogJzMyJywgZ29hbHM6IDAsIGdhbWVzOiAzNCwgeDogLTEwMCwgeTogMzAwIH1cbiAgICAgICAgICAgIHsgbmFtZTogJ0Nhc2lsbGFzJywgYXNzZXQ6ICdybS1jYXNpbGxhcy5qcGcnLCBvcmlnaW46ICdTcGFpbicsIGhlaWdodDogJzEuODVtJywgc2hpcnQ6ICcxJywgcG9zOiAnR29hbGllJywgZG9iOiAnMzQnLCBnb2FsczogMCwgZ2FtZXM6IDQ4LCB4OiAwLCB5OiA0MTAgfVxuICAgICAgICBdXG5cbnN0YXRlID1cbiAgICBob21lOiB0cnVlXG4gICAgZGlzYWJIb3ZlcjogZmFsc2VcbiAgICBzd2FwU2lkZXM6IC0+XG4gICAgICAgIGlmIEBob21lIHRoZW4gQGhvbWUgPSBmYWxzZSBlbHNlIEBob21lID0gdHJ1ZVxuICAgIGN1clNpZGU6IC0+XG4gICAgICAgIGlmIEBob21lIHRoZW4gJ2hvbWUnIGVsc2UgJ2F3YXknXG5cbnBvcyA9XG4gICAgd29ybGQ6XG4gICAgICAgIGJhc2VYOiAwXG4gICAgICAgIGJhc2VZOiAwXG4gICAgICAgIGJhc2VaOiAtMjAwXG4gICAgZGVmOlxuICAgICAgICBnb2FsaWU6IFswLC01MF1cblxuZG9tID1cbiAgICBhZGRQbGF5ZXJzOiAoc2lkZSkgLT5cbiAgICAgICAgZm9yIGtleSwgdmFsIG9mIGRhdGEucGxheWVyc1tzaWRlXVxuICAgICAgICAgICAgdmFsLnNpZGU9IHNpZGVcbiAgICAgICAgICAgICRlbCA9IEBhZGRQbGF5ZXIgdmFsXG4gICAgICAgICAgICAkdGVhbS5hcHBlbmQgJGVsXG5cbiAgICAgICAgJHBsYXllcnMgPSAkKCcuanMtcGxheWVyJylcbiAgICAgICAgJHBsYXllcnNIb21lID0gJCgnLmpzLXBsYXllcltkYXRhLXNpZGU9XCJob21lXCJdJylcbiAgICAgICAgJHBsYXllcnNBd2F5ID0gJCgnLmpzLXBsYXllcltkYXRhLXNpZGU9XCJhd2F5XCJdJylcblxuXG4gICAgYWRkUGxheWVyOiAoZGF0YSkgLT5cbiAgICAgICAgJGVsID0gJCAnPGRpdiBjbGFzcz1cImpzLXBsYXllciBwbGF5ZXJcIiBkYXRhLW5hbWU9XCInICsgZGF0YS5uYW1lICsgJ1wiIGRhdGEtc2lkZT1cIicgKyBkYXRhLnNpZGUgKyAnXCIgZGF0YS14PVwiJyArIGRhdGEueCArICdcIiBkYXRhLXk9XCInICsgZGF0YS55ICsgJ1wiPjwvZGl2PidcbiAgICAgICAgJGVsLmFwcGVuZCAnPGRpdiBjbGFzcz1cInBsYXllcl9fbGFiZWxcIj48c3Bhbj4nICsgZGF0YS5uYW1lICsgJzwvc3Bhbj48L2Rpdj4nXG4gICAgICAgICRlbC5hcHBlbmQgJzxkaXYgY2xhc3M9XCJwbGF5ZXJfX2ltZ1wiPjxpbWcgc3JjPSAnICsgQVNTRVRfVVJMICsgZGF0YS5hc3NldCArICc+PC9kaXY+J1xuICAgICAgICAkZWwucHJlcGVuZCAnPGRpdiBjbGFzcz1cInBsYXllcl9fY2FyZFwiPiA8L2Rpdj4nXG4gICAgICAgICRlbC5wcmVwZW5kICc8ZGl2IGNsYXNzPVwicGxheWVyX19wbGFjZWhvbGRlclwiPjwvZGl2PidcbiAgICAgICAgQHBvcHVsYXRlQ2FyZCAkZWwuZmluZCgnLnBsYXllcl9fY2FyZCcpLCBkYXRhXG4gICAgICAgICRlbFxuXG4gICAgcHJlbG9hZEltYWdlczogKHByZWxvYWQpIC0+XG4gICAgICAgIHByb21pc2VzID0gW11cbiAgICAgICAgaSA9IDBcbiAgICAgICAgd2hpbGUgaSA8IHByZWxvYWQubGVuZ3RoXG4gICAgICAgICAgKCh1cmwsIHByb21pc2UpIC0+XG4gICAgICAgICAgICBpbWcgPSBuZXcgSW1hZ2VcbiAgICAgICAgICAgIGltZy5vbmxvYWQgPSAtPiBwcm9taXNlLnJlc29sdmUoKVxuICAgICAgICAgICAgaW1nLnNyYyA9IHVybFxuICAgICAgICAgICkgcHJlbG9hZFtpXSwgcHJvbWlzZXNbaV0gPSAkLkRlZmVycmVkKClcbiAgICAgICAgICBpKytcbiAgICAgICAgJC53aGVuLmFwcGx5KCQsIHByb21pc2VzKS5kb25lIC0+XG4gICAgICAgICAgICBzY2VuZXMuZW5kTG9hZGluZygpXG4gICAgICAgICAgICBzY2VuZXMubG9hZEluKDE2MDApXG5cblxuICAgIHBvcHVsYXRlQ2FyZDogKCRlbCwgZGF0YSkgLT5cbiAgICAgICAgJGVsLmFwcGVuZCAnPGgzPicgKyBkYXRhLm5hbWUgKyAnPC9oMz4nICtcbiAgICAgICAgICAgICc8dWwgY2xhc3M9XCJwbGF5ZXJfX2NhcmRfX2xpc3RcIj48bGk+PHNwYW4+RE9CPC9zcGFuPjxici8+JyArIGRhdGEuZG9iICsgJyB5cjwvbGk+PGxpPjxzcGFuPkhlaWdodDwvc3Bhbj48YnIvPicgKyBkYXRhLmhlaWdodCArICc8L2xpPjxsaT48c3Bhbj5PcmlnaW48L3NwYW4+PGJyLz4nICsgZGF0YS5vcmlnaW4gKyAnPC9saT48L3VsPicgK1xuICAgICAgICAgICAgJzx1bCBjbGFzcz1cInBsYXllcl9fY2FyZF9fbGlzdCBwbGF5ZXJfX2NhcmRfX2xpc3QtLWxhc3RcIj48bGk+PHNwYW4+R2FtZXM8L3NwYW4+PGJyLz4nICsgZGF0YS5nYW1lcyArICc8L2xpPjxsaT48c3Bhbj5Hb2Fsczwvc3Bhbj48YnIvPicgKyBkYXRhLmdvYWxzICsgJzwvbGk+PC91bD4nXG5cbiAgICBkaXNwbGF5Tm9uZTogKCRlbCkgLT5cbiAgICAgICAgJGVsLmNzcyAnZGlzcGxheScsICdub25lJ1xuXG5ldmVudHMgPVxuICAgIGF0dGFjaEFsbDogLT5cbiAgICAgICAgJHN3aXRjaEJ0bi5vbiAnY2xpY2snLCAoZSkgLT5cbiAgICAgICAgICAgIGUucHJldmVudERlZmF1bHQoKVxuICAgICAgICAgICAgJGVsID0gJCh0aGlzKVxuICAgICAgICAgICAgcmV0dXJuIGlmICRlbC5oYXNDbGFzcyAnZGlzYWJsZWQnXG4gICAgICAgICAgICBzY2VuZXMuc3dpdGNoU2lkZXMoKVxuICAgICAgICAgICAgJHN3aXRjaEJ0bi5yZW1vdmVDbGFzcyAnZGlzYWJsZWQnXG4gICAgICAgICAgICAkZWwuYWRkQ2xhc3MgJ2Rpc2FibGVkJ1xuXG4gICAgICAgICRsb2FkQnRuLm9uICdjbGljaycsIChlKSAtPlxuICAgICAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpXG4gICAgICAgICAgICBzY2VuZXMubG9hZEluKClcblxuICAgICAgICAkcGxheWVycy5vbiAnY2xpY2snLCAoZSkgLT5cbiAgICAgICAgICAgIGUucHJldmVudERlZmF1bHQoKVxuICAgICAgICAgICAgJGVsID0gJCh0aGlzKVxuICAgICAgICAgICAgaWYgJCgnLmFjdGl2ZScpLmxlbmd0aCB0aGVuIHJldHVybiBmYWxzZVxuICAgICAgICAgICAgJGVsLmFkZENsYXNzICdhY3RpdmUnXG4gICAgICAgICAgICBzY2VuZXMuZm9jdXNQbGF5ZXIoJGVsKVxuICAgICAgICAgICAgc2V0VGltZW91dCAoIC0+IGV2ZW50cy5hdHRhY2hDbG9zZSgpKSwgMVxuXG4gICAgYXR0YWNoQ2xvc2U6IC0+XG4gICAgICAgICRzdGFnZS5vbmUgJ2NsaWNrJywgKGUpIC0+XG4gICAgICAgICAgICBlLnByZXZlbnREZWZhdWx0KClcbiAgICAgICAgICAgIHNjZW5lcy51bmZvY3VzUGxheWVyKClcblxuc2NlbmVzID1cbiAgICBwcmVMb2FkOiAtPlxuICAgICAgICAkdGVhbUxpc3RIb21lLnZlbG9jaXR5IHsgb3BhY2l0eTogMCB9LCAwXG4gICAgICAgICRwbGF5ZXJzLnZlbG9jaXR5IHsgb3BhY2l0eTogMCB9LCAwXG4gICAgICAgICRsb2FkQnRuLnZlbG9jaXR5IHsgb3BhY2l0eTogMCB9LCAwXG4gICAgICAgICRzd2l0Y2hlci52ZWxvY2l0eSB7IG9wYWNpdHk6IDAgfSwgMFxuICAgICAgICAkaGVhZGluZy52ZWxvY2l0eSB7IG9wYWNpdHk6IDAgfSwgMFxuICAgICAgICAkc3ViSGVhZGluZy52ZWxvY2l0eSB7IG9wYWNpdHk6IDAgfSwgMFxuICAgICAgICAkcGxheWVyc0F3YXkuY3NzICdkaXNwbGF5JywgJ25vbmUnXG4gICAgICAgICR3b3JsZC52ZWxvY2l0eSB7IG9wYWNpdHk6IDAsIHRyYW5zbGF0ZVo6IC0yMDAsIHRyYW5zbGF0ZVk6IC02MCB9LCAwXG4gICAgICAgICQoJ21haW4nKS52ZWxvY2l0eSB7IG9wYWNpdHk6IDEgfSwgMFxuXG4gICAgbG9hZEluOiAoZGVsYXkgPSAwKSAtPlxuICAgICAgICAkd29ybGQudmVsb2NpdHkgeyBvcGFjaXR5OiAxLCB0cmFuc2xhdGVZOiAwLCB0cmFuc2xhdGVaOiAtMjAwIH0sIHsgZHVyYXRpb246IDEwMDAsIGRlbGF5OiBkZWxheSwgZWFzaW5nOiAnc3ByaW5nJyB9XG4gICAgICAgIGFuaW0uZmFkZUluRGlyKCRoZWFkaW5nLCAzMDAsIChkZWxheSArIDYwMCksIDAsIDMwKVxuICAgICAgICBhbmltLmZhZGVJbkRpcigkc3ViSGVhZGluZywgMzAwLCAoZGVsYXkgKyA4MDApLCAwLCAzMClcbiAgICAgICAgYW5pbS5mYWRlSW5EaXIoJHRlYW1MaXN0SG9tZSwgMzAwLCAoZGVsYXkgKyA4MDApLCAwLCAzMClcbiAgICAgICAgYW5pbS5mYWRlSW5EaXIoJHN3aXRjaGVyLCAzMDAsIChkZWxheSArIDkwMCksIDAsIDMwKVxuXG4gICAgICAgIGRlbGF5ICs9IDEyMDBcbiAgICAgICAgZGVsYXlJbmMgPSAzMFxuICAgICAgICBhbmltLmRyb3BQbGF5ZXJzKCRwbGF5ZXJzSG9tZSwgZGVsYXksIGRlbGF5SW5jKVxuXG4gICAgc3RhcnRMb2FkaW5nOiAtPlxuICAgICAgICBhbmltLmZhZGVJbkRpciAkbG9hZGluZywgMzAwLCAwLCAwLCAtMjBcbiAgICAgICAgaW1hZ2VzID0gW11cbiAgICAgICAgZm9yIGtleSwgdmFsIG9mIGRhdGEucGxheWVycy5ob21lIGFuZCBkYXRhLnBsYXllcnMuYXdheVxuICAgICAgICAgICAgaW1hZ2VzLnB1c2ggQVNTRVRfVVJMICsgdmFsLmFzc2V0XG5cbiAgICAgICAgZG9tLnByZWxvYWRJbWFnZXMoaW1hZ2VzKVxuXG4gICAgZW5kTG9hZGluZzogLT5cbiAgICAgICAgYW5pbS5mYWRlT3V0RGlyICRsb2FkaW5nLCAzMDAsIDEwMDAsIDAsIC0yMFxuXG4gICAgYXJyYW5nZVBsYXllcnM6IC0+XG4gICAgICAgICRwbGF5ZXJzLmVhY2ggLT5cbiAgICAgICAgICAgICRlbCA9ICQodGhpcylcblxuICAgICAgICAgICAgJGVsLnZlbG9jaXR5XG4gICAgICAgICAgICAgICAgdHJhbnNsYXRlWDogcGFyc2VJbnQgJGVsLmF0dHIoJ2RhdGEteCcpXG4gICAgICAgICAgICAgICAgdHJhbnNsYXRlWjogcGFyc2VJbnQgJGVsLmF0dHIoJ2RhdGEteScpICMgWiBpcyB0aGUgWSBheGlzIG9uIHRoZSBmaWVsZFxuXG4gICAgZm9jdXNQbGF5ZXI6ICgkZWwpIC0+XG4gICAgICAgIGRhdGEgPSAkZWwuZGF0YSgpXG4gICAgICAgIHNoaWZ0WSA9IGRhdGEueVxuXG4gICAgICAgIGlmIHNoaWZ0WSA+IDAgdGhlbiBzaGlmdFkgPSAoZGF0YS55IC8gMilcblxuICAgICAgICAkKCcuanMtcGxheWVyW2RhdGEtc2lkZT1cIicgKyBzdGF0ZS5jdXJTaWRlKCkgKyAnXCJdJykubm90KCcuYWN0aXZlJykuZWFjaCAtPlxuICAgICAgICAgICAgJHVuZm9jdXMgPSAkKHRoaXMpXG4gICAgICAgICAgICBhbmltLmZhZGVPdXREaXIgJHVuZm9jdXMsIDMwMCwgMCwgMCwgMCwgMCwgbnVsbCwgMC4yXG5cbiAgICAgICAgJHdvcmxkLnZlbG9jaXR5XG4gICAgICAgICAgICB0cmFuc2xhdGVYOiAocG9zLndvcmxkLmJhc2VYIC0gZGF0YS54KVxuICAgICAgICAgICAgdHJhbnNsYXRlWTogKHBvcy53b3JsZC5iYXNlWSlcbiAgICAgICAgICAgIHRyYW5zbGF0ZVo6IChwb3Mud29ybGQuYmFzZVogLSBzaGlmdFkpICMgWiBpcyB0aGUgWSBheGlzIG9uIHRoZSBmaWVsZFxuXG4gICAgICAgICwgNjAwXG5cbiAgICAgICAgJHRlcnJhaW4udmVsb2NpdHlcbiAgICAgICAgICAgIG9wYWNpdHk6IDAuNjZcbiAgICAgICAgLCA2MDBcblxuICAgICAgICBAc2hvd1BsYXllckNhcmQgJGVsLCA2MDAsIDYwMFxuXG4gICAgdW5mb2N1c1BsYXllcjogLT5cbiAgICAgICAgJGVsID0gJCgnLmpzLXBsYXllci5hY3RpdmUnKVxuICAgICAgICBkYXRhID0gJGVsLmRhdGEoKVxuICAgICAgICBhbmltLmZhZGVJbkRpciAkKCcuanMtcGxheWVyW2RhdGEtc2lkZT1cIicgKyBzdGF0ZS5jdXJTaWRlKCkgKyAnXCJdJykubm90KCcuYWN0aXZlJyksIDMwMCwgMzAwLCAwLCAwLCAwLCBudWxsLCAwLjJcbiAgICAgICAgJGVsLnJlbW92ZUNsYXNzICdhY3RpdmUnXG4gICAgICAgICR3b3JsZC52ZWxvY2l0eVxuICAgICAgICAgICAgdHJhbnNsYXRlWDogKHBvcy53b3JsZC5iYXNlWClcbiAgICAgICAgICAgIHRyYW5zbGF0ZVk6IChwb3Mud29ybGQuYmFzZVkpXG4gICAgICAgICAgICB0cmFuc2xhdGVaOiAocG9zLndvcmxkLmJhc2VaKSAjIFogaXMgdGhlIFkgYXhpcyBvbiB0aGUgZmllbGRcblxuICAgICAgICAsIDYwMFxuXG4gICAgICAgICR0ZXJyYWluLnZlbG9jaXR5XG4gICAgICAgICAgICBvcGFjaXR5OiAxXG4gICAgICAgICwgNjAwXG5cbiAgICAgICAgQGhpZGVQbGF5ZXJDYXJkICRlbCwgNjAwLCA2MDBcblxuICAgIGhpZGVQbGF5ZXJDYXJkOiAoJGVsLCBkdXIsIGRlbGF5KSAtPlxuICAgICAgICAkY2FyZCA9ICRlbC5maW5kICcucGxheWVyX19jYXJkJ1xuICAgICAgICAkaW1hZ2UgPSAkZWwuZmluZCAnLnBsYXllcl9faW1nJ1xuICAgICAgICAkaW1hZ2UudmVsb2NpdHlcbiAgICAgICAgICAgIHRyYW5zbGF0ZVk6IDBcbiAgICAgICAgLCAzMDBcbiAgICAgICAgYW5pbS5mYWRlSW5EaXIgJGVsLmZpbmQgJy5wbGF5ZXJfX2xhYmVsJywgMjAwLCBkZWxheVxuICAgICAgICBhbmltLmZhZGVPdXREaXIgJGNhcmQsIDMwMCwgMCwgMCwgLTEwMFxuXG4gICAgc2hvd1BsYXllckNhcmQ6ICgkZWwsIGR1ciwgZGVsYXkpIC0+XG4gICAgICAgICRjYXJkID0gJGVsLmZpbmQgJy5wbGF5ZXJfX2NhcmQnXG4gICAgICAgICRpbWFnZSA9ICRlbC5maW5kICcucGxheWVyX19pbWcnXG4gICAgICAgICRpbWFnZS52ZWxvY2l0eVxuICAgICAgICAgICAgdHJhbnNsYXRlWTogJy09MTUwcHgnXG4gICAgICAgICwgMzAwXG4gICAgICAgIGFuaW0uZmFkZU91dERpciAkZWwuZmluZCAnLnBsYXllcl9fbGFiZWwnLCAyMDAsIGRlbGF5XG4gICAgICAgIGFuaW0uZmFkZUluRGlyICRjYXJkLCAzMDAsIDIwMCwgMCwgMTAwXG5cbiAgICBzd2l0Y2hTaWRlczogLT5cbiAgICAgICAgZGVsYXkgPSAwXG4gICAgICAgIGRlbGF5SW5jID0gMjBcblxuICAgICAgICAkb2xkID0gJHBsYXllcnNIb21lXG4gICAgICAgICRuZXcgPSAkcGxheWVyc0F3YXlcbiAgICAgICAgaWYgIXN0YXRlLmhvbWVcbiAgICAgICAgICAgICRvbGQgPSAkcGxheWVyc0F3YXlcbiAgICAgICAgICAgICRuZXcgPSAkcGxheWVyc0hvbWVcblxuICAgICAgICBzdGF0ZS5zd2FwU2lkZXMoKVxuXG4gICAgICAgICRvbGQuZWFjaCAtPlxuICAgICAgICAgICAgJGVsID0gJCh0aGlzKVxuICAgICAgICAgICAgYW5pbS5mYWRlT3V0RGlyKCRlbCwgMjAwLCBkZWxheSwgMCwgLTYwLCAwKVxuICAgICAgICAgICAgYW5pbS5mYWRlT3V0RGlyKCRlbC5maW5kKCcucGxheWVyX19sYWJlbCcpLCAyMDAsIChkZWxheSArIDcwMCkpXG4gICAgICAgICAgICBkZWxheSArPSBkZWxheUluY1xuXG4gICAgICAgICR0ZXJyYWluLnZlbG9jaXR5IHsgcm90YXRlWTogJys9MTgwZGVnJyB9LCB7IGRlbGF5OiAxNTAsIGR1cmF0aW9uOiAxMjAwIH1cbiAgICAgICAgYW5pbS5kcm9wUGxheWVycygkbmV3LCAxNTAwLCAzMClcblxuYW5pbSA9XG4gICAgZmFkZUluRGlyOiAoJGVsLCBkdXIsIGRlbGF5LCBkZWx0YVggPSAwLCBkZWx0YVkgPSAwLCBkZWx0YVogPSAwLCBlYXNpbmcgPSBudWxsLCBvcGFjaXR5ID0gMCkgLT5cbiAgICAgICAgJGVsLmNzcyAnZGlzcGxheScsICdibG9jaydcblxuICAgICAgICAkZWwudmVsb2NpdHlcbiAgICAgICAgICAgIHRyYW5zbGF0ZVg6ICctPScgKyBkZWx0YVhcbiAgICAgICAgICAgIHRyYW5zbGF0ZVk6ICctPScgKyBkZWx0YVlcbiAgICAgICAgICAgIHRyYW5zbGF0ZVo6ICctPScgKyBkZWx0YVpcbiAgICAgICAgLCAwXG5cbiAgICAgICAgJGVsLnZlbG9jaXR5XG4gICAgICAgICAgICBvcGFjaXR5OiAxXG4gICAgICAgICAgICB0cmFuc2xhdGVYOiAnKz0nICsgZGVsdGFYXG4gICAgICAgICAgICB0cmFuc2xhdGVZOiAnKz0nICsgZGVsdGFZXG4gICAgICAgICAgICB0cmFuc2xhdGVaOiAnKz0nICsgZGVsdGFaXG4gICAgICAgICxcbiAgICAgICAgICAgIGVhc2luZzogZWFzaW5nXG4gICAgICAgICAgICBkZWxheTogZGVsYXlcbiAgICAgICAgICAgIGR1cmF0aW9uOiBkdXJcblxuICAgIGZhZGVPdXREaXI6ICgkZWwsIGR1ciwgZGVsYXksIGRlbHRhWCA9IDAsIGRlbHRhWSA9IDAsIGRlbHRhWiA9IDAsIGVhc2luZyA9IG51bGwsIG9wYWNpdHkgPSAwKSAtPlxuICAgICAgICBpZiAhb3BhY2l0eVxuICAgICAgICAgICAgZGlzcGxheSA9ICdub25lJ1xuICAgICAgICBlbHNlXG4gICAgICAgICAgICBkaXNwbGF5ID0gJ2Jsb2NrJ1xuXG4gICAgICAgICRlbC52ZWxvY2l0eVxuICAgICAgICAgICAgb3BhY2l0eTogb3BhY2l0eVxuICAgICAgICAgICAgdHJhbnNsYXRlWDogJys9JyArIGRlbHRhWFxuICAgICAgICAgICAgdHJhbnNsYXRlWTogJys9JyArIGRlbHRhWVxuICAgICAgICAgICAgdHJhbnNsYXRlWjogJys9JyArIGRlbHRhWlxuICAgICAgICAsXG4gICAgICAgICAgICBlYXNpbmc6IGVhc2luZ1xuICAgICAgICAgICAgZGVsYXk6IGRlbGF5XG4gICAgICAgICAgICBkdXJhdGlvbjogZHVyXG4gICAgICAgIC52ZWxvY2l0eVxuICAgICAgICAgICAgb3BhY2l0eTogb3BhY2l0eVxuICAgICAgICAgICAgdHJhbnNsYXRlWDogJy09JyArIGRlbHRhWFxuICAgICAgICAgICAgdHJhbnNsYXRlWTogJy09JyArIGRlbHRhWVxuICAgICAgICAgICAgdHJhbnNsYXRlWjogJy09JyArIGRlbHRhWlxuICAgICAgICAsXG4gICAgICAgICAgICBkdXJhdGlvbjogMFxuICAgICAgICAgICAgZGlzcGxheTogZGlzcGxheVxuXG5cbiAgICBkcm9wUGxheWVyczogKCRlbHMsIGRlbGF5LCBkZWxheUluYykgLT5cbiAgICAgICAgJGVscy5lYWNoIC0+XG4gICAgICAgICAgICAkZWwgPSAkKHRoaXMpXG4gICAgICAgICAgICAkZWwuY3NzXG4gICAgICAgICAgICAgICAgZGlzcGxheSA6ICdibG9jaydcbiAgICAgICAgICAgICAgICBvcGFjaXR5IDogMFxuXG4gICAgICAgICAgICBhbmltLmZhZGVJbkRpcigkZWwsIDgwMCwgZGVsYXksIDAsIDUwLCAwLCAnc3ByaW5nJylcbiAgICAgICAgICAgIGFuaW0uZmFkZUluRGlyKCRlbC5maW5kKCcucGxheWVyX19sYWJlbCcpLCAyMDAsIChkZWxheSArIDI1MCkpXG4gICAgICAgICAgICBkZWxheSArPSBkZWxheUluY1xuXG5pbml0ID0gLT5cbiAgICAkc3RhZ2UgICAgICAgID0gJCgnLmpzLXN0YWdlJylcbiAgICAkd29ybGQgICAgICAgID0gJCgnLmpzLXdvcmxkJylcbiAgICAkc3dpdGNoQnRuICAgID0gJCgnLmpzLXN3aXRjaCcpXG4gICAgJGxvYWRCdG4gICAgICA9ICQoJy5qcy1sb2FkJylcbiAgICAkaGVhZGluZyAgICAgID0gJCgnLmpzLWhlYWRpbmcnKVxuICAgICRzd2l0Y2hlciAgICAgPSAkKCcuanMtc3dpdGNoZXInKVxuICAgICRjbG9zZUJ0biAgICAgPSAkKCcuanMtY2xvc2UnKVxuICAgICRzdWJIZWFkaW5nICAgPSAkKCcuanMtc3ViaGVhZGluZycpXG4gICAgJHRlcnJhaW4gICAgICA9ICQoJy5qcy10ZXJyYWluJylcbiAgICAkdGVhbSAgICAgICAgID0gJCgnLmpzLXRlYW0nKVxuICAgICR0ZWFtTGlzdEhvbWUgPSAkKCcuanMtdGVhbS1ob21lJylcbiAgICAkbG9hZGluZyAgICAgID0gJCgnLmpzLWxvYWRpbmcnKVxuXG4gICAgZG9tLmFkZFBsYXllcnMoJ2hvbWUnKVxuICAgIGRvbS5hZGRQbGF5ZXJzKCdhd2F5JylcbiAgICBzY2VuZXMucHJlTG9hZCgpXG4gICAgc2NlbmVzLmFycmFuZ2VQbGF5ZXJzKClcbiAgICBldmVudHMuYXR0YWNoQWxsKClcbiAgICBzY2VuZXMuc3RhcnRMb2FkaW5nKClcblxuJChkb2N1bWVudCkucmVhZHkgLT5cbiAgICBpbml0KCkiXX0=
//# sourceURL=coffeescript