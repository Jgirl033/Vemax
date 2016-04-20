

读取Json文件：（jsonfilepath是.json文件的物理路径）
 StreamReader sr = File.OpenText(jsonfilepath);
 StringBuilder jsonArrayText_tmp = new StringBuilder();
 string input = null;
 while ((input = sr.ReadLine()) != null)
 {
            jsonArrayText_tmp.Append(input);
 }
 sr.Close();
 string jsonArrayText = jsonArrayText_tmp.Replace(" ", "").ToString();



string jsonText = @"{""input"" : ""value"", ""output"" : ""result""}";
JsonReader reader=new JsonTextReader(new StringReader(jsonText));
while(reader.Read())
{
       Console.WriteLine(reader.TokenType + "\t\t" + reader.ValueType + "\t\t" + reader.Value);
}

JObject jo = JObject.Parse(jsonText);
string[] values = jo.Properties().Select(item => item.Value.ToString()).ToArray();




string jsonArrayText1 = "[{'a':'a1','b':'b1'},{'a':'a2','b':'b2'}]";
JArray ja = (JArray)JsonConvert.DeserializeObject(jsonArrayText1);
string ja1a = ja[1]["a"].ToString();

JObject o = (JObject)ja[1];
string oa = o["a"].ToString();


string jsonText = "{"beijing":{"zone":"海淀","zone_en":"haidian"}}";
JObject jo = (JObject)JsonConvert.DeserializeObject(jsonText);
string zone = jo["beijing"]["zone"].ToString();
string zone_en = jo["beijing"]["zone_en"].ToString();


@param {Object} loadingOption

showLoading: function (loadingOption)
{
      public string Input{get;set;}
      public string Output{set;get;}

Project p = new Project() { Input = "stone", Output = "gold" };
 JsonSerializer serializer = new JsonSerializer();
StringWriter sw = new StringWriter();
serializer.Serialize(new JsonTextWriter(sw), p);
Console.WriteLine(sw.GetStringBuilder().ToString());

JavaScriptSerializer serializer = new JavaScriptSerializer();
var json = serializer.Serialize(p);
 var p1 = serializer.Deserialize(json);
Project p1 = (Project)serializer.Deserialize(new JsonTextReader(sr), typeof(Project));


}

