#!/usr/bin/env ruby

# 生成完整的数据,在有默认值时.
def generate_complete_array(h)
  res_array = []
  h.each_key { |k|
    h[k]['title'] = k unless h[k].include?('title')
    # rev[k]['comment'] = 'nothing' unless rev[k].include?('comment')
    # puts h[k]
    res_array.push(h[k])
  }
  return res_array
end

def generate_valid_str(s)
  begin_value = s.split('_')[0].split('[')[1].to_s
  end_value = s.split('_')[1].split(']')[0].to_s
  res_array = []
  (begin_value..end_value).each { |i|
    now_str = s.gsub(/\[\d{1,}_\d{1,}\]/, i)
    res_array.push(now_str)
  }
  return res_array
end

# 展开一个hash数据,此方法接收一个hash数据,返回一个展开后的list数据
def expansions_hash(a)
  new_ip, new_title, new_alias, each_size_by_new_array, res = [], [], [], [], []
  a.each { |k, v|
    if v.to_s.match(/\[\d{1,}_\d{1,}\]/)
      new_ip    = generate_valid_str(v) if k == 'ip'
      new_title = generate_valid_str(v) if k == 'title'
      new_alias = generate_valid_str(v) if k == 'host_aliases'
    else
      new_ip << a[k] if k == 'ip'
      new_title << a[k] if k == 'title'
      new_alias << a[k] if k == 'host_aliases'
    end
  }
  # 不需要展开时, 以数组形式返回原始数据
  return res << a if new_ip.size == 1 && new_title.size == 1 && new_alias.size == 1

  # 如果展开长度不一致,以最小长度字段为准:
  each_size_by_new_array << new_ip.size if new_ip.size > 1
  each_size_by_new_array << new_title.size if new_title.size > 1
  each_size_by_new_array << new_alias.size if new_alias.size > 1
  latest_size = each_size_by_new_array.min - 1
  (0 .. latest_size).each { |c|
    res << { 'ip' => new_ip[c], 'title' => new_title[c], 'host_aliases' => new_alias[c] }
  }

  # 如果此字段不必展开,则填入原始数据
  res.each{ |r|
    r['ip'] = new_ip[0] if r['ip'].to_s.empty?
    r['title'] = new_title[0] if r['title'].to_s.empty?
    r['host_aliases'] = new_alias[0] if r['host_aliases'].to_s.empty?
  }
  return res
end

#
def main(h)
  res = []
  h.each { |a| res += expansions_hash(a) }
  return res
end


input = {
    'demo.bw-y.com' => {
        'ip'           => '192.168.10.[9_12]',
        'host_aliases' => 'demo ceph-osd',
    },
    'lab[01_03].bw-y.com' => {
        'ip'           => '10.0.0.[21_23]',
        'host_aliases' => 'lab[01_02]',
    },
    'test.bw-y.com' => {
        'ip'           => '172.16.0.20',
        'host_aliases' => 'test',
    }
}

res = main(generate_complete_array(input))
print 'input: ', input, "\n"
puts '###########################'
print 'print output: ', res, "\n"
puts '###########################'
puts 'puts output: ', res
