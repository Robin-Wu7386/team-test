// src/composables/useHerbPool.js
import { ref } from 'vue'

export const herbList = ref([
  {
    id: 1,
    name: '当归',
    category: '补血',
    brief: '补血活血，调经止痛，润肠通便。适用于血虚萎黄，眩晕心悸。',
    shortTags: ['补血', '调经', '活血'],
    categoryId: 'xue'
  },
  {
    id: 2,
    name: '枸杞',
    category: '滋阴',
    brief: '滋补肝肾，益精明目。适用于肝肾阴虚，头晕目眩，视力减退。',
    shortTags: ['滋阴', '明目', '养肝'],
    categoryId: 'yin'
  },
  {
    id: 3,
    name: '人参',
    category: '补气',
    brief: '大补元气，复脉固脱，益气健脾。适用于体虚欲脱，肢冷脉微。',
    shortTags: ['补气', '安神', '健脾'],
    categoryId: 'qi'
  },
  {
    id: 4,
    name: '鹿茸',
    category: '补阳',
    brief: '壮肾阳，益精血，强筋骨。适用于肾阳不足，精血亏虚，阳痿滑精。',
    shortTags: ['补阳', '益精', '强骨'],
    categoryId: 'yang'
  },
  {
    id: 5,
    name: '金银花',
    category: '清热',
    brief: '清热解毒，疏散风热。适用于痈肿疔疮，喉痹，丹毒，风热感冒。',
    shortTags: ['清热', '解毒', '解表'],
    categoryId: 'qingre'
  },
  {
    id: 6,
    name: '薏米',
    category: '祛湿',
    brief: '利水渗湿，健脾止泻，清热排脓。适用于水肿，脚气，小便不利。',
    shortTags: ['祛湿', '健脾', '消肿'],
    categoryId: 'qushi'
  },
  {
    id: 7,
    name: '麦冬',
    category: '滋阴',
    brief: '养阴生津，润肺清心。适用于肺燥干咳，阴虚痨嗽，津伤口渴。',
    shortTags: ['滋阴', '润肺', '生津'],
    categoryId: 'yin'
  },
  {
    id: 8,
    name: '肉桂',
    category: '补阳',
    brief: '补火助阳，引火归元，散寒止痛。适用于阳痿宫冷，腰膝冷痛。',
    shortTags: ['补阳', '散寒', '止痛'],
    categoryId: 'yang'
  }
])

export function useHerbPool() {
  return { herbList }
}
