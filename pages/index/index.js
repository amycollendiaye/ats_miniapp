Page({

  data: {
    isFocus: false,
    DataZones:[
      {id:1, zone:'Tous' ,size:"100rpx"},
      {id:2, zone:'Dakar', size:"100rpx"},
      {id:3, zone:'saly', size:"100rpx"},
      {id:4, zone:'Lompoul', size:"120rpx"},
      {id:5, zone:'Saint-Louis', size:"150rpx"},
      {id:6, zone:'Experience locale', size:"200rpx"}

    ],
    tabs: [
      { 
        key: 'accueil', 
        slotName: 'tab-accueil', 
        contentSlot: 'content-accueil' 
      },
      { 
        key: 'explorer', 
        slotName: 'tab-explorer', 
        contentSlot: 'content-explorer' 
      },
      { 
        key: 'favoris', 
        slotName: 'tab-favoris', 
        contentSlot: 'content-favoris' 
      },
      { 
        key: 'agenda', 
        slotName: 'tab-agenda', 
        contentSlot: 'content-agenda' 
      }
    ]
  },

  
  onFocus() {
    this.setData({
       isFocus:true
      // isFocus: !this.data.isFocus
    })
  },

  onBlur() {
    this.setData({
      isFocus: false
    })
  },

  onLoad() {},
  onReady() {},
  onShow() {},
  onHide() {},
  onUnload() {}

})