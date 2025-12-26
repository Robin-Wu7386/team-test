// 中药显示顺序
export const HERB_DISPLAY_ORDER = [
  '药材名称','拼音注音','英文名','别名','来源','出处','来源书籍',
  '性味','归经','性味归经','功能主治','用法用量','药理作用','临床应用',
  '主要成分','化学成分','含量测定','原形态','植物形态','动物形态',
  '性状','鉴别','炮制','制法','制剂','药用部位','采收加工',
  '生境分布','栽培','毒性','注意','各家论述','复方','相关药方',
  '摘录','备注','贮藏','规格'
];

// 方剂显示顺序 + 属性映射
export const FANGJI_DISPLAY_ORDER = ['方剂名称', '处方', '制法', '功能主治', '用法用量', '注意', '摘录'];

export const FANGJI_PROP_MAP = {
  'prescription': '处方',
  'preparation': '制法',
  'function': '功能主治',
  'usage': '用法用量',
  'caution': '注意',
  'excerpt': '摘录'
};

// 历史记录key
export const HISTORY_KEY = 'herb_history';